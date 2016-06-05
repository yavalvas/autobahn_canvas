# -*- coding: utf-8 -*-

"""Приложение Twisted."""
import txaio
txaio.use_twisted()
from twisted.internet import reactor



# инициализация

import canvas_server
canvas_server.server_runner()

application = canvas_server.application
