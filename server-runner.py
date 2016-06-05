#!/usr/bin/python
from twisted.scripts.twistd import run
import canvas_server
from os.path import join, dirname
import os
from sys import argv
app_file = os.path.join(".", 'canvas_server.py')
logfile = os.path.join(".", 'server.log')
tacfile = os.path.join(".", 'server.tac')
pid = os.path.join(".", 'chess_server.pid')

argv[1:] = [
    '-y', tacfile,
    '--pidfile', pid,
    '--logfile', logfile
]
run()
