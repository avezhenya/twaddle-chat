#!/usr/bin/python
#  -*- coding: utf-8 -*-
import logging
import os
import time
import uuid

import redis
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from config import BaseConfig as Config
from tornado.escape import json_encode, json_decode, to_basestring
from tornado.ioloop import PeriodicCallback
from tornado.options import define, options
from utils import spam_links, replace_smiles

r = redis.StrictRedis(host=Config.HOST, port=Config.PORT, db=0)
define("port", default=8889, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/ignore", IgnoreHandler),
            (r"/chatsocket", ChatSocketHandler),
            (r'/(favicon\.ico)', tornado.web.StaticFileHandler,
             {'path': '/static/favicon.ico'})
        ]
        settings = dict(
            cookie_secret=Config.SECRET,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=Config.COOKIES, # TODO(avezhenya) Need improvement
            debug=Config.DEBUG,
            autoreload=Config.AUTORELOAD,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        """ Return all messages for room """
        user = self.get_argument('u', 'NoName')
        if user == "":
            user = 'NoName'
        room = self.get_argument('r', False)
        if user in Config.USERNAME_IGNORE_LIST:
            user = 'user-{}'.format(str(uuid.uuid4())[:7])
        if user and room:
            keys = r.lrange(room + ':msg', 0, -1)
            if len(keys) != 0:
                messages = r.mget(keys)
                messages.reverse()
                messages = [json_decode(i) for i in messages if i is not None]
            else:
                messages = keys
            self.render('index.html',
                        messages=messages, user=user)
        else:
            self.send_error(404, reason='Incorrect params of query')

    def post(self):
        """ Send system message in room, for attention users """
        room = self.get_argument('r', False)
        user = self.get_argument('u', False)
        message = self.get_argument('msg', 'no message')
        if not room or not user or user != 'system':
            raise tornado.web.HTTPError(404, 'Incorrect params of query')
        logging.info('Got system message {0}, room "{1}"'.format(message, room))
        chat = {
            "id": str(uuid.uuid4()),
            "body": message,
            "user": user,
            "time": str(int(time.time()))
        }
        chat['html'] = to_basestring(
            self.render_string('system_message.html', message=chat)
        )
        ChatSocketHandler.update_cache(chat, room)
        ChatSocketHandler.send_updates(chat, room)


class IgnoreHandler(tornado.web.RequestHandler):

    def get(self):
        """ Return object with lists all users and ignore """
        room = self.get_argument('room', False)
        user = self.get_argument('user', False)
        if not user or not room:
            return self.write({'status': False})
        result = {'user': user, 'ignore': [], 'users_list': []}
        if room + ':clients' in ChatSocketHandler.waiters:
            for usr in ChatSocketHandler.waiters[room + ':clients']:
                if usr[1] != '' and usr[1] not in result['users_list']:
                    result['users_list'].append(usr[1])
        if r.exists(user + ':ignore'):
            tmp = [i.decode("utf-8") for i in r.lrange(user + ':ignore', 0, -1)]
            result['ignore'] += tmp
        self.write(result)

    def post(self):
        """ Add any unwelcome users in personal ignore list for user """
        req = {'user': self.get_argument('user', False),
               'ignore': json_decode(self.get_argument('ignore', False))}
        if not req['user'] or req['ignore'] == False:
            return self.write({'status': False})
        if len(req['ignore']):
            if r.exists(req['user'] + ':ignore'):
                r.delete(req['user'] + ':ignore')
                r.lpush(req['user'] + ':ignore', *req['ignore'])
                r.expire(req['user'] + ':ignore', Config.USER_BAN_LIST_TIMEOUT)
            else:
                r.lpush(req['user'] + ':ignore', *req['ignore'])
                r.expire(req['user'] + ':ignore', Config.USER_BAN_LIST_TIMEOUT)
        elif r.exists(req['user'] + ':ignore'):
            r.delete(req['user'] + ':ignore')
        return self.write({'status': True})


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = {}

    def open(self):
        """
        It performed at the time of connection of client and server in this
         case, at the time of downloading web pages.
        Add client to 'waiters set' depending on the room.
        """
        room = self.get_argument('r', False)
        user = self.get_argument('u', '')
        if room:
            if room + ':clients' not in ChatSocketHandler.waiters.keys():
                ChatSocketHandler.waiters[room + ':clients'] = set()
            ChatSocketHandler.waiters[room + ':clients'].add((self, user))
            msg = {'len': len(ChatSocketHandler.waiters[room + ':clients'])}
            ChatSocketHandler.send_updates(msg, room)
            logging.info('Client +1 into room "{}"'.format(room))
        else:
            self.send_error(404, reason='Incorrect params of query')

    def on_close(self):
        """
        Performed in the closing or update web page.
        Remove client from 'waiters set' depending on the room.
        """
        room = self.get_argument('r', False)
        user = self.get_argument('u', '')
        if room:
            ChatSocketHandler.waiters[room + ':clients'].remove((self, user))
            msg = {'len': len(ChatSocketHandler.waiters[room + ':clients'])}
            ChatSocketHandler.send_updates(msg, room)
            logging.info('Client -1 from room "{}"'.format(room))
            # TODO(avezhenya) If empty set, need to delete it or expire 3600 sec
        else:
            self.send_error(404, reason='Incorrect params of query')
        # print(ChatSocketHandler.waiters)

    @classmethod
    def send_updates(cls, chat, room):
        """ All clients receive messages
        :param room:
        :param chat:
        """
        if room + ':clients' in cls.waiters.keys():
            logging.info("Sending message to %d waiters",
                         len(cls.waiters[room + ':clients']))
            for waiter in cls.waiters[room + ':clients']:
                try:
                    waiter[0].write_message(chat)
                except:
                    logging.error('Error sending message', exc_info=True)

    @classmethod
    def update_cache(cls, chat, room):
        """
        Storing messages in memory with a pool in the last 100 messages
        :param room:
        :param chat:
        """
        key = '{}:{}'.format(room, chat['id'][:7])
        r.setex(key, Config.ROOM_CLEAR_TIMEOUT, json_encode(chat))
        r.lpush(room + ':msg', key)  # TODO(avezhenya) Need to merge in Pipeline
        if r.llen(room + ':msg') > Config.CACHE_SIZE:  # Meybe it's not need
            r.ltrim(room + ':msg', 0, Config.CACHE_SIZE)

    @classmethod
    def pinging(cls):
        """ Send ping message to client."""
        for clients in cls.waiters.values():
            for client in clients:
                client[0].ping(b'Ping')

    def on_message(self, message):
        """ Performed when a message arrives from a client
        :param message:
        """
        room = self.get_argument('r', False)
        if not room:
            raise tornado.web.HTTPError(404, 'Incorrect params of query')
        logging.info('Got message {0} for room "{1}"'.format(message, room))
        parsed = json_decode(message)
        parsed['body'] = replace_smiles(spam_links(parsed['body']))
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed['body'],
            "user": parsed['user'],
            "time": str(int(time.time()))
        }
        chat['html'] = to_basestring(
            self.render_string('message.html', message=chat)
        )
        # put it in cache and give to listeners
        ChatSocketHandler.update_cache(chat, room)
        ChatSocketHandler.send_updates(chat, room)

    def on_pong(self, data):
        """
        Invoked when the response to a ping frame is received.
        :param data:
        """
        if data != b'Ping':
            self.close(reason='Bad message on_pong')
            logging.info('Connection with client {} was closed'.format(self))


def main():
    tornado.options.parse_command_line()
    logging.info("Server started")  # TODO(avezhenya) Add log file
    app = Application()
    app.listen(options.port)
    PeriodicCallback(ChatSocketHandler.pinging, 50000).start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
