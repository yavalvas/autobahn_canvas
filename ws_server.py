# -*- coding: utf-8 -*-
from autobahn.twisted.websocket import WebSocketServerFactory, \
     WebSocketServerProtocol, listenWS
import json, cgi
from twisted.internet import reactor

class BroadcastServerProtocol(WebSocketServerProtocol):
    """
    Протокол сервера
    """
    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        """
        При открытии вебсокета регистрируем текущий протокол
        :return:
        """
        self.factory.register(self)
    def onMessage(self, payload, isBinary):
        msg = json.loads(payload)
        print "MSG", msg
        print msg.get('current_coord')
        self.factory.change_my_coord(self, msg.get('current_coord'))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
        
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

class BroadcastServerFactory(WebSocketServerFactory):
    """
    Для обмена сообщениями с клиентом
    """

    def __init__(self, url=None, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = {}
        
    def change_my_coord(self, client, coord):
        self.clients[client]=coord
        self.broadcast(coord)

    def register(self, client):
        #новый клиент не среди существующих (клиент как ip)
        if not client in self.clients:
            print("FULL Client", client);
            print("registered client {}".format(client.peer))
            self.clients[client] = [250, 195]
            print self.clients

    def unregister(self, client):
        if client in self.clients:
            del self.clients[client]

    def broadcast(self, msg, skip=None):
        msg = self.clients.values()
        for client in self.clients:
            print(client)
            full_struct = {"cube_info": msg, "player_ip": client.peer}
            result = json.dumps(full_struct, ensure_ascii=False).encode('utf-8')
            client.sendMessage(result)
