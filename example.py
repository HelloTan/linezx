# -*- coding: utf-8 -*-
import LINEZX
from tcr.ttypes import *
from datetime import datetime
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast

cl = LINEZX.LINE()
cl.login(qr=True)
cl.loginResult()
#cl.login(token='TOKEN MU')
#cl.loginResult()

def BOT(op):
    try:
        if op.type == 0:
            return
        if op.type == 25:
            msg = op.message
            pesan = msg.text
            pengirim = msg._from
            to = msg.to	
            if pesan is None:
                return
            if pesan.lower() == "sp":
                start = time.time()
                cl.sendText(to, "Testing....")
                elapsed_time = time.time() - start
                cl.sendText(to, "%s detik" % (elapsed_time))
    except Exception as error:
        print(error)
	
while True:
    BOT(cl.polling())
