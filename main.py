#coding=utf-8

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("What's your name?".encode('utf-8'))

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        name = name.decode('utf-8')
        if name in self.users:
            self.sendLine("Name taken, please choose another.")
            return
        msg = "Welcome, %s!" % (name)
        self.sendLine(msg.encode('utf-8'))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = message.decode('utf-8')
        message = "<%s> %s" % (self.name,message)
        for name, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(message.encode('utf-8'))


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Chat(self.users)

reactor.listenTCP(8888, ChatFactory())
reactor.run()