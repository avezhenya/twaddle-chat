import os


class BaseConfig(object):
    """
    CACHE_SIZE - How much messages can be in room at the same time.
    ROOM_CLEAR_TIMEOUT - Maximum storage time for message.
    ROOM_REMOVE_TIMEOUT - Maximum storage time for room when it don't have
        clients.
    USER_BAN_LIST_TIMEOUT - Maximum storage time for user ban list.
    USERNAME_IGNORE_LIST - List of prohibited names.
    PATTERN_1 - pattern for bad words (Russian language)
    PATTERN_2 - pattern for bad words (Russian language)
    PATTERN_3 - pattern for replace all links from message
    """
    # System settings
    DEBUG = True
    AUTORELOAD = True
    COOKIES = True
    SECRET = '[+\x9dpg\xf4\xd18\xfb\x94kq\x19\xa6\xdb\x87)0\xe1\xdd\x1b>P\xf3'
    if os.getenv('PROD', False):
        HOST = os.environ.get('REDISHOST_PORT_6379_TCP_ADDR')
        PORT = int(os.environ.get('REDISHOST_PORT_6379_TCP_PORT'))
        DEBUG = False
    else:
        HOST = '192.168.99.100'
        PORT = '6379'

    # Settings for chat
    CACHE_SIZE = 100
    ROOM_CLEAR_TIMEOUT = 3600  # 1 hour
    ROOM_REMOVE_TIMEOUT = 3600  # 1 hour
    USER_BAN_LIST_TIMEOUT = 43200  # 12 hours
    USERNAME_IGNORE_LIST = ['admin', 'system', 'administrator', 'moderator',
                            'False', 'True']
    SMILES = {':balloon:': 'balloon',
              ':salute:': 'salute',
              ':ball:': 'ball',
              ':cow:': 'cow',
              ':up:': 'up',
              ':yes:': 'up',
              ':down:': 'down',
              ':no:': 'down',
              ':shit:': 'shit',
              ':smile:': 'smile',
              ':)': 'smile',
              '=)': 'smile2',
              '(:': 'smile',
              ':]': 'smile',
              ':}': 'smile',
              ':-)': 'smile',
              ':-]': 'smile',
              ':-}': 'smile',
              ':o)': 'smile2',
              ':о)': 'smile2',
              ':с)': 'smile2',
              ':c)': 'smile2',
              ':^)': 'smile2',
              ':-D': 'smile3',
              ':D': 'smile3',
              '=D': 'smile3',
              'xD': 'smile3',
              'XD': 'smile3',
              'хД': 'smile3',
              'ХД': 'smile3',
              ':tongue:': 'tongue',
              ':-P': 'tongue',
              ':-p': 'tongue',
              ':-Р': 'tongue',
              ':-р': 'tongue',
              ':-b': 'tongue',
              ':-Þ': 'tongue',
              ':-9': 'tongue',
              ':P': 'tongue',
              ':p': 'tongue',
              ':Р': 'tongue',
              ':р': 'tongue',
              ':Þ': 'tongue',
              '=P': 'tongue',
              '=p': 'tongue',
              '=Р': 'tongue',
              '=р': 'tongue',
              '=b': 'tongue',
              '=Þ': 'tongue',
              ':9': 'tongue',
              ':-/': 'smile83',
              ':-\\': 'smile83',
              ':/': 'smile83',
              ':\\': 'smile83',
              ':cry:': 'cry',
              ':\'(': 'cry',
              ':,(': 'cry',
              ':dude:': 'dude',
              '8-)': 'dude',
              'B-)': 'dude',
              'В-)': 'dude',
              'в-)': 'dude',
              '8)': 'dude',
              'B)': 'dude',
              'В)': 'dude',
              'в)': 'dude',
              '8-D': 'dude',
              'B-D': 'dude',
              'В-D': 'dude',
              'в-D': 'dude',
              '8D': 'dude',
              'BD': 'dude',
              'ВD': 'dude',
              'вD': 'dude',
              ':surprise:': 'surprise',
              '8O': 'surprise',
              '8o': 'surprise',
              '8О': 'surprise',
              '8о': 'surprise',
              ':-0': 'surprise',
              ':-O': 'surprise',
              ':-o': 'surprise',
              ':-О': 'surprise',
              ':-о': 'surprise',
              ':0': 'surprise',
              ':O': 'surprise',
              ':o': 'surprise',
              ':О': 'surprise',
              ':о': 'surprise',
              ':|': 'smile81',
              '=|': 'smile82',
              'T_T': 'TT',
              '^_^': 'mm',
              '^__^': 'mm',
              ':what:': 'what',
              'O_o': 'what',
              'o_o': 'what',
              'O_O': 'what',
              '0_o': 'what',
              'o_O': 'what',
              'o_0': 'what',
              'о_0': 'what',
              'О_О': 'what',
              'О_о': 'what',
              '0_о': 'what',
              'о_о': 'what',
              'X0': 'what',
              'XO': 'what',
              'ХО': 'what',
              'Х0': 'what',
              ':sad:': 'sad',
              ':(': 'sad',
              '=(': 'sad',
              '):': 'sad',
              ':[': 'sad',
              ':{': 'sad',
              ':-(': 'sad',
              '=-(': 'sad',
              ')-:': 'sad',
              ':-[': 'sad',
              ':-{': 'sad',
              ':wink:': 'wink',
              ';)': 'wink',
              ';D': 'wink',
              ';]': 'wink',
              ':devil:': 'devil',
              '>:)': 'devil',
              '>:D': 'devil',
              ':evil:': 'angry',
              ':angry:': 'angry',
              '>:(': 'angry',
              ':angel:': 'angel',
              '0:)': 'angel',
              '0:-)': 'angel',
              '0:-D': 'angel',
              '0:^)': 'angel',
              ':love:': 'love',
              '<3': 'love',
              '<з': 'love',
              '<З': 'love',
              ':kiss:': 'kiss',
              ':-*': 'kiss',
              ':*': 'kiss',
              ':^*': 'kiss',
              ':sunny:': 'sun',
              ':sun:': 'sun',
              ':rain:': 'rain',
              ':coffee:': 'coffee',
              ':cloud:': 'cloud'
              }
    PATTERN_1 = r''.join((
        r'\w{0,5}[хx]([хx\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[уy]([уy\s\!@#\$%\^&*+-\|\/]{0,6})[ёiлeеюийя]\w{0,7}|\w{0,6}[пp]',
        r'([пp\s\!@#\$%\^&*+-\|\/]{0,6})[iие]([iие\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[3зс]([3зс\s\!@#\$%\^&*+-\|\/]{0,6})[дd]\w{0,10}|[сcs][уy]',
        r'([уy\!@#\$%\^&*+-\|\/]{0,6})[4чkк]\w{1,3}|\w{0,4}[bб]',
        r'([bб\s\!@#\$%\^&*+-\|\/]{0,6})[lл]([lл\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[yя]\w{0,10}|\w{0,8}[её][bб][лске@eыиаa][наи@йвл]\w{0,8}|\w{0,4}[еe]',
        r'([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[uу]([uу\s\!@#\$%\^&*+-\|\/]{0,6})[н4ч]\w{0,4}|\w{0,4}[еeё]',
        r'([еeё\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[нn]([нn\s\!@#\$%\^&*+-\|\/]{0,6})[уy]\w{0,4}|\w{0,4}[еe]',
        r'([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[оoаa@]([оoаa@\s\!@#\$%\^&*+-\|\/]{0,6})[тnнt]\w{0,4}|\w{0,10}[ё]',
        r'([ё\!@#\$%\^&*+-\|\/]{0,6})[б]\w{0,6}|\w{0,4}[pп]',
        r'([pп\s\!@#\$%\^&*+-\|\/]{0,6})[иeеi]([иeеi\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[дd]([дd\s\!@#\$%\^&*+-\|\/]{0,6})[oоаa@еeиi]',
        r'([oоаa@еeиi\s\!@#\$%\^&*+-\|\/]{0,6})[рr]\w{0,12}'))
    PATTERN_2 = r'|'.join((
        r"(\b[сs]{1}[сsц]{0,1}[uуy](?:[ч4]{0,1}[иаakк][^ц])\w*\b)",
        r"(\b(?!пло|стра|[тл]и)(\w(?!(у|пло)))*[хx][уy](й|йа|[еeё]|и|я|ли|ю)"
        r"(?!га)\w*\b)",
        r"(\b(п[oо]|[нз][аa])*[хx][eе][рp]\w*\b)",
        r"(\b[мm][уy][дd]([аa][кk]|[oо]|и)\w*\b)",
        r"(\b\w*д[рp](?:[oо][ч4]|[аa][ч4])(?!л)\w*\b)",
        r"(\b(?!(?:кило)?[тм]ет)(?!смо)[а-яa-z]*(?<!с)т[рp][аa][хx]\w*\b)",
        r"(\b[к|k][аaoо][з3z]+[eе]?ё?л\w*\b)",
        r"(\b(?!со)\w*п[еeё]р[нд](и|иc|ы|у|н|е|ы)\w*\b)",
        r"(\b\w*[бп][ссз]д\w+\b)",
        r"(\b([нnп][аa]?[оo]?[xх])\b)",
        r"(\b([аa]?[оo]?[нnпбз][аa]?[оo]?)?([cс][pр][аa][^зжбсвм])\w*\b)",
        r"(\b\w*([оo]т|вы|[рp]и|[оo]|и|[уy]){0,1}([пnрp][iиеeё]{0,1}[3zзсcs]"
        r"[дd])\w*\b)",
        r"(\b(вы)?у?[еeё]?би?ля[дт]?[юоo]?\w*\b)",
        r"(\b(?!вело|ски|эн)\w*[пpp][eеиi][дd][oaоаеeирp](?![цянгюсмйчв])[рp]?"
        r"(?![лт])\w*\b)",
        r"(\b(?!в?[ст]{1,2}еб)(?:(?:в?[сcз3о][тяaа]?[ьъ]?|вы|п[рp][иоo]|[уy]"
        r"|р[aа][з3z][ьъ]?|к[оo]н[оo])?[её]б[а-яa-z]*)|(?:[а-яa-z]*[^хлрдв]"
        r"[еeё]б)\b)",
        r"(\b[з3z][аaоo]л[уy]п[аaeеин]\w*\b)"))
    PATTERN_3 = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                 '(?:%[0-9a-fA-F][0-9a-fA-F]))+')
