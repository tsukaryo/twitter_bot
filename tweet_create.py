# -*- encoding:utf-8 -*-

import markov
from distutils.util import strtobool
import logging
from requests_oauthlib import OAuth1Session
import requests
import json
import sys
import os
import re
import MeCab
import random

# Mecabによってわかちがきを行う


def wakati(text):
    # 余計な文字列を除去
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text = re.sub('RT', "", text)
    text = re.sub('#kana_nishino', "", text)
    text = re.sub('/', "", text)
    text = re.sub('#西野カナ', "", text)
    t = MeCab.Tagger("-Owakati")
    m = t.parse(text)
    result = m.rstrip(" \n").split(" ")
    return result

# 連鎖数3のマルコフ連鎖にて文章生成


def create_tw():
    """
python learn.py <filename> [format] [max_chars] [min_chars]
filename: Do not include .txt or .json etc.
"""

    logger = logging.getLogger(__name__)
    fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=fmt)

    args = sys.argv

    print('Usage: python learn.py <filename> [format] [max_chars] [min_chars]')

    try:
        filename = args[1]
    except IndexError:
        print('ERROR: filename is required. (e.g. "sample")')
        sys.exit()

    format = bool(strtobool(args[2])) if args[2:3] else True
    max_chars = int(args[3]) if args[3:4] else 70
    min_chars = int(args[4]) if args[4:5] else 25

    """
    1. Load text -> Parse text using MeCab
    """
    parsed_text = markov.parse_text('data/' + filename + '.txt')
    logger.info('Parsed text.')

    """
    2. Build model
    """
    text_model = markov.build_model(parsed_text, format=format, state_size=4)
    logger.info('Built text model.')

    json = text_model.to_json()
    open('data/' + filename + '.json', 'w').write(json)

# Load from JSON
# json = open('input.json').read()
# text_model = markovify.Text.from_json(json)

    """
    3. Make sentences
    """
    try:
        # for _ in range(30):
        sentence = markov.make_sentences(
            text_model, start='', max=max_chars, min=min_chars)
        logger.info(sentence)
    except KeyError:
        logger.error('KeyError: No sentence starts with "start".')
        logger.info(
            'If you set format=True, please change "start" to another word.')
        logger.info('If you set format=False, you cannot specify "start".')

    return sentence

# main関数


def main():
    CK = 'RMmf9efk2sipYb1FszQ8GUCGY'
    CS = 'T6ocguR4gL6kJHpJaDvsQjhTzOk3ZYOGRk8hIGCQ4aVKjFkOCw'
    AT = '1223574767954878464-krM3gMDeDbDQCbefXYgsFgv1QbwxpE'
    AS = 'gBNg5g12H9VOImlthv7KE73ia0x1bxi7i5JIJTWAhbTJ9'

    #filename = "input.txt"
    #src = open(filename, "r").read()
    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"
    # わかち書き
    #wordlist = wakati(src)
    # 文の作成
    tw = create_tw()
    tw_ha = '#名言\n'
    tw = tw_ha+tw
    # ツイート本文
    params = {"status": tw}
    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(url, params=params)
    # レスポンスを確認
    if req.status_code == 200:
        print("posted tweet:" + tw)
    else:
        print("Error: %d" % req.status_code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
