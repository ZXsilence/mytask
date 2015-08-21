#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: dongxuanliang
@contact: dongxuanliang@maimiaotech.com
@date: 2015-08-21 13:22
@version: 2015
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import base64
from Crypto.Cipher import AES

#SECRTE_KEY长度为16, 24, or 32
SECRET_KEY = '^&maimiaotech!@#'
BLOCK_SIZE = len(SECRET_KEY)
PADDING = '{'

def generate_ticket(nick,worker_id,article_code,timestamp):
    s = 'nick:%s, worker_id:%s, article_code:%s, timestamp:%s' % (nick,worker_id,article_code,timestamp)
    return encode_AES(s)

def encode_AES(encode_str):
    cipher = AES.new(SECRET_KEY)
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    return EncodeAES(cipher, encode_str)


def decode_AES(decode_str):
    cipher = AES.new(SECRET_KEY)
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    return DecodeAES(cipher, decode_str)

if __name__ == '__main__':
    import time
    ticket = generate_ticket('chinchinstyle',11,'ts-1796606',time.time())
    print ticket
    print decode_AES(ticket)
