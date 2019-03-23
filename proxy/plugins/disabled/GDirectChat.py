##########
# HEADER
# AUTHOR: DOTX | HUGO A.
##########

import commands, plugins, packetFactory
import os, json, struct, time
import config
import data.clients as dataclients
import data.players as dataplayers
from config import ShipLabel
from config import YAMLConfig
from PSO2DataTools import check_irc_with_pso2
from PSO2DataTools import check_pso2_with_irc
from PSO2DataTools import replace_irc_with_pso2
from PSO2DataTools import replace_pso2_with_irc
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.internet import task
from twisted.python import log
from twisted.words.protocols import irc

try:
    import PSO2PDConnector
    redisEnabled = True
except ImportError:
    redisEnabled = False
	
ircSettings = YAMLConfig("cfg/gchat-irc.config.yml",
                         {'enabled': False, 'nick': "PSO2IRCBot", 'server': '', 'port': 6667, 'svname': 'NickServ', 'svpass': '', 'channel': "", 'output': True, 'autoexec': []}, True)
						
ircBot = None
ircMode = ircSettings.get_key('enabled')
ircOutput = ircSettings.get_key('output')
ircNick = ircSettings.get_key('nick')
ircServer = (ircSettings.get_key('server'), ircSettings.get_key('port'))
ircChannel = ircSettings.get_key('channel')
ircServicePass = ircSettings.get_key('svpass')
ircServiceName = ircSettings.get_key('svname')

gchatSettings = YAMLConfig("cfg/gchat.config.yml", {'displayMode': 0, 'bubblePrefix': '', 'systemPrefix': '{whi}', 'prefix': ''}, True)						
						 
def doRedisGchat(message):
    gchatMsg = json.loads(message['data'])
    fb = ("SHIP-%02i") % gchatMsg['ship']
    shipl = ShipLabel.get(fb, fb)
    strgchatmsg = str(gchatMsg['text'].encode('utf-8'))
    if not check_irc_with_pso2(strgchatmsg):
        return
    if gchatMsg['server'] == PSO2PDConnector.connector_conf['server_name']:
        return
    if gchatMsg['sender'] == 1:
        for client in dataclients.connectedClients.values():
            if client.preferences.get_preference('globalChat') and client.get_handle() is not None:
                if lookup_gchatmode(client.preferences) == 0:
                    client.get_handle().send_crypto_packet(packetFactory.TeamChatPacket(gchatMsg['playerId'], "[Discord] %s" % gchatMsg['playerName'], "[Discord] %s" % gchatMsg['playerName'], "%s%s" % (client.preferences.get_preference('globalChatPrefix'), replace_irc_with_pso2(strgchatmsg).decode('utf-8', 'ignore'))).build())
                else:
                    client.get_handle().send_crypto_packet(packetFactory.SystemMessagePacket("[Discord] <%s> %s" % (gchatMsg['playerName'], "%s%s" % (client.preferences.get_preference('globalChatPrefix'), replace_irc_with_pso2(strgchatmsg).decode('utf-8', 'ignore'))), 0x3).build())
    else:
        if ircMode:
                global ircBot
                if ircBot is not None:
                    ircBot.send_global_message(gchatMsg['ship'], str(gchatMsg['playerName'].encode('utf-8')), strgchatmsg, str(gchatMsg['server']))
        for client_data in dataclients.connectedClients.values():
                if client_data.preferences.get_preference('globalChat') and client_data.get_handle() is not None:
                    if lookup_gchatmode(client_data.preferences) == 0:
                        client_data.get_handle().send_crypto_packet(packetFactory.TeamChatPacket(gchatMsg['playerId'], "(%s) [%s] %s" % (gchatMsg['server'], shipl, gchatMsg['playerName']), gchatMsg['playerName'], "%s%s" % (client_data.preferences.get_preference('globalChatPrefix'), gchatMsg['text'])).build())
                    else:
                        client_data.get_handle().send_crypto_packet(packetFactory.SystemMessagePacket("(%s) [%s] <%s> %s" % (gchatMsg['server'], shipl, gchatMsg['playerName'], "%s%s" % (client_data.preferences.get_preference('globalChatPrefix'), gchatMsg['text'])), 0x3).build())

if redisEnabled:
    PSO2PDConnector.thread.pubsub.subscribe(**{'plugin-message-gchat': doRedisGchat})

if ircMode:
    # noinspection PyUnresolvedReferences
    class GChatIRC(irc.IRCClient):
        currentPid = 0
        userIds = {}

        def __init__(self):
            global ircNick
            self.nickname = ircNick
            self.ircOutput = ircOutput

        def get_user_id(self, user):
            if user not in self.userIds:
                self.userIds[user] = self.currentPid
                self.currentPid += 1
            return self.userIds[user]

        def connectionMade(self):
            irc.IRCClient.connectionMade(self)
            print("[GlobalChat] IRC Connected!")

        def connectionLost(self, reason):
            irc.IRCClient.connectionLost(self, reason)
            print("[GlobalChat] IRC Connection lost!")

        def joinChan(self):
            global ircBot
            try:
                if self.factory.channel[:1] in ["#", "!", "+", "&"]:
                    self.join(self.factory.channel)
                    print("[GlobalChat] Joined %s" % self.factory.channel)
                    ircBot = self
                else:
                    raise NameError("[GlobalChat] Failed to join %s channel must contain a #, !, + or & before the channel name" % self.factory.channel)
            except NameError as ne:
                print(ne)
                log.msg(ne)

        def signedOn(self):
            for command in ircSettings.get_key('autoexec'):
                self.sendLine(command)
                print("[IRC-AUTO] >>> %s" % command)
            task.deferLater(reactor, 15, self.joinChan)
            print("[GlobalChat] Joining channels in 15 seconds...")

        def privmsg(self, user, channel, msg):
            if not check_irc_with_pso2(msg):
                return
            if channel == self.factory.channel:
                if self.ircOutput is True:
                    print("[GlobalChat] [Discord] <%s> %s" % (user.split("!")[0], replace_irc_with_pso2(msg).decode('utf-8', 'ignore')))
                if redisEnabled:
                    PSO2PDConnector.db_conn.publish("plugin-message-gchat", json.dumps({'sender': 1, 'text': replace_irc_with_pso2(msg).decode('utf-8', 'ignore'), 'server': PSO2PDConnector.connector_conf['server_name'], 'playerName': user.split("!")[0], 'playerId': self.get_user_id(user.split("!")[0])}))
                for client in data.clients.connectedClients.values():
                    if client.preferences.get_preference('globalChat') and client.get_handle() is not None:
                        if lookup_gchatmode(client.preferences) == 0:
                            client.get_handle().send_crypto_packet(packetFactory.TeamChatPacket(self.get_user_id(user.split("!")[0]), "[Discord] %s" % user.split("!")[0], "[Discord] %s" % user.split("!")[0], "%s%s" % (client.preferences.get_preference('globalChatPrefix'), replace_irc_with_pso2(msg).decode('utf-8', 'ignore'))).build())
                        else:
                            client.get_handle().send_crypto_packet(packetFactory.SystemMessagePacket("[Discord] <%s> %s" % (user.split("!")[0], "%s%s" % (client.preferences.get_preference('globalChatPrefix'), replace_irc_with_pso2(msg).decode('utf-8', 'ignore'))), 0x3).build())
            else:
                print("[Discord] <%s> %s" % (user, msg))

        def noticed(self, user, channel, message):
            print("[Discord] [NOTICE] %s %s" % (user, message))
            if user.split("!")[0] == 'NickServ' and 'registered' in message:
                global ircServicePass
                global ircServiceName
                if ircServicePass is not '':
                    self.msg(ircServiceName, "identify %s" % (ircServicePass))
                    print("[Discord] Sent identify command to %s." % (ircServiceName))

        def action(self, user, channel, msg):
            if not check_irc_with_pso2(msg):
                return
            if channel == self.factory.channel:
                if self.ircOutput is True:
                    print("[GlobalChat] [Discord] * %s %s" % (user, replace_irc_with_pso2(msg).decode('utf-8', 'ignore')))
                for client in data.clients.connectedClients.values():
                    if client.preferences.get_preference('globalChat') and client.get_handle() is not None:
                        if lookup_gchatmode(client.preferences) == 0:
                            client.get_handle().send_crypto_packet(packetFactory.TeamChatPacket(self.get_user_id(user.split("!")[0]), "[Discord] %s" % user.split("!")[0], "[Discord] %s" % user.split("!")[0], "* %s%s" % (client.preferences.get_preference('globalChatPrefix'), replace_irc_with_pso2(msg).decode('utf-8', 'ignore'))).build())
                        else:
                            client.get_handle().send_crypto_packet(packetFactory.SystemMessagePacket("[Discord] <%s> * %s" % (user.split("!")[0], "%s%s" % (client.preferences.get_preference('globalChatPrefix'), replace_irc_with_pso2(msg).decode('utf-8', 'ignore'))), 0x3).build())

        def send_global_message(self, ship, user, message1, server=None):
            if not check_pso2_with_irc(message1):
                return
            fb = ("SHIP-%02i") % ship
            shipl = ShipLabel.get(fb, fb)
            if server is None:
                self.msg(self.factory.channel, "[%s] <%s> %s" % (shipl, user, replace_pso2_with_irc(message1)))
            else:
                self.msg(self.factory.channel, "(%s) [%s] <%s> %s" % (server, shipl, user, replace_pso2_with_irc(message1)))

        def send_channel_message(self, message):
            self.msg(self.factory.channel, message)

    class GIRCFactory(protocol.ClientFactory):
        """docstring for ClassName"""

        def __init__(self, channel):
            self.channel = channel

        def buildProtocol(self, addr):
            p = GChatIRC()
            p.factory = self
            return p

        def clientConnectionLost(self, connector, reason):
            connector.connect()

        def clientConnectionFailed(self, connector, reason):
            connector.connect()
			
def lookup_gchatmode(client_preferences):
    if client_preferences['gchatMode'] is not -1:
        return client_preferences['gchatMode']
    return 1


@plugins.CommandHook("grelay", "Chat di Global Chat tanpa perintah !g")
class GChatDirectCfg(commands.Command):
    def call_from_client(self, client):
        idsega = client.myUsername
        if idsega is None or str(idsega) == "None" or idsega == "None":
            client.send_crypto_packet(packetFactory.SystemMessagePacket("[Command] Tidak dapat menggunakan perintah ini dikarenakan anda adalah (Someone) atau (None) user.", 0x3).build())
        else:
            preferences = dataclients.ClientPreferences(idsega)
            if preferences.has_preference("chatMuted") and preferences.get_preference('chatMuted'):
                client.send_crypto_packet(packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}Gchat anda berstatus: {gre}OFF {red}sehingga tidak dapat menggunakan Gchat.", 0x3).build())
                return
            if preferences.has_preference("globalChatDirect"): isActive = preferences.get_preference("globalChatDirect")
            else: isActive = True #reverse mode
            isActive = not isActive
            preferences.set_preference("globalChatDirect", isActive)
            if isActive:
                client.send_crypto_packet(packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}Direct Global Chat diaktifkan. {red}PERHATIAN !!! {gre}Chat apapun baik AUTOWORD maupun yang kamu kirim ke Area/Party/Team akan auto send ke Global Chat !", 0x3).build())
            else:
                client.send_crypto_packet(packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}Direct Global Chat dinonaktifkan.", 0x3).build())


@plugins.PacketHook(0x7, 0x0)
def GChatDirect(context, data):
    """
    :type context: ShipProxy.ShipProxy
    """
    idsega = context.myUsername
    if idsega is None or str(idsega) == "None" or idsega == "None":
        return data
    else:
        pref = dataclients.ClientPreferences(idsega)
        if pref.has_preference("globalChatDirect"):
            isActive = pref.get_preference("globalChatDirect")
            if isActive:
                if pref.has_preference("chatMuted") and pref.get_preference('chatMuted'):
                    pref.set_preference("globalChatDirect", False)
                    isActive = False
        else: isActive = False
        if isActive:
            try:
                player_id = struct.unpack_from('I', data, 0x8)[0]
                message1 = data[0x1C:].decode('utf-16')
                if player_id == 0:
                    message1 = message1.rstrip('\0')
                    if message1.startswith("/"): return data
                    player_name = dataplayers.playerList[context.playerId][0].rstrip('\0')
                    fb = ("SHIP-%02i") % dataclients.connectedClients[context.playerId].ship
                    shipl = ShipLabel.get(fb, fb)
                    tUser = "[%s] <%s>" % (shipl, player_name)
                    print("[GlobalChat] <%s> %s" % (dataplayers.playerList[context.playerId][0], message1))
		if redisEnabled:
					PSO2PDConnector.db_conn.publish("plugin-message-gchat", json.dumps({'sender': 0, 'text': message1, 'server': PSO2PDConnector.connector_conf['server_name'], 'playerName': dataplayers.playerList[context.playerId][0], 'playerId': client.playerId, 'ship': dataclients.connectedClients[client.playerId].ship}))
		if ircMode:
			global ircBot
			if ircBot is not None:
				ircBot.send_global_message1(dataclients.connectedClients[context.playerId].ship, dataplayers.playerList[context.playerId][0].encode('utf-8'), message1.encode('utf-8'))
			for client_data in dataclients.connectedClients.values():
				if client_data.preferences.get_preference('globalChat') and client_data.get_handle() is not None:
					if lookup_gchatmode(client_data.preferences) == 0:
						client_data.get_handle().send_crypto_packet(packetFactory.TeamChatPacket(context.playerId, "[%s] %s" % (shipl, player_name), player_name, "%s%s" % (client_data.preferences.get_preference('globalChatPrefix'), message1)).build())
					else:
						client_data.get_handle().send_crypto_packet(packetFactory.SystemMessagePacket("{ora}[%s] <%s>{yel} %s" % (shipl, player_name, "%s%s" % (client_data.preferences.get_preference('globalChatPrefix'), message)), 0x3).build())
			return None
            except Exception as e:
                print("[Error] %s" % e)
                return data
        return data
