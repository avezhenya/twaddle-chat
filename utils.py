#!usr/bin/python
# -*- coding: utf-8 -*-
from config import BaseConfig
import re


smiles = BaseConfig.SMILES
pattern_1 = re.compile(BaseConfig.PATTERN_2, re.U | re.I)
pattern_3 = re.compile(BaseConfig.PATTERN_3)


def spam_links(msg):
    """
    Replace all links for smile
    :param msg
    """
    result = re.findall(pattern_3, msg)
    for i in result:
        msg = msg.replace(i, ':shit:')
    msg = regexp_proc(msg, repl=' :shit: ')
    return msg


def replace_smiles(msg):
    """
    Replace all smiles for <span> tag
    :param msg
    """
    for k, v in smiles.items():
        msg = msg.replace(k, '<span class="emoji emoji-{}"></span>'.format(v))
    return msg


def regexp_proc(msg, repl='[censured]'):
    """Replace all bad words (Russian language)
    :param msg
    :param repl
    """
    return pattern_1.sub(repl, msg)
