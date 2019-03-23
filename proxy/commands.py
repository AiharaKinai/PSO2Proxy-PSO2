import calendar
import cProfile
import data.blocks
import data.clients
import data.players
import datetime
import pstats
import shutil
import sys
from twisted.internet import reactor
from twisted.python import rebuild

useFaulthandler = True

try:
    import faulthandler
except ImportError:
    useFaulthandler = False

import config
import packetFactory
import plugins.plugins as plugin_manager
from ShipProxy import ShipProxy


commandList = {}


class CommandHandler(object):
    def __init__(self, command_name, help_text=None, admin_conly=False):
        self.commandName = command_name
        self.help_text = help_text
        self.admin_only = admin_conly

    def __call__(self, command_class):
        global commandList
        commandList[self.commandName] = [command_class, self.help_text, self.admin_only]


class Command(object):
    def __init__(self, args=None):
        self.args = args

    def call_from_client(self, client):
        """
        :param client: ShipProxy.ShipProxy
        """
<<<<<<< HEAD
        client.send_crypto_packet(packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}Perintah tidak dapat digunakan di PSO2.", 0x3).build())
=======
        client.send_crypto_packet(
            packetFactory.SystemMessagePacket(
                "[Command] {red}That command cannot be run in-game.",
                0x3
            ).build()
        )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00

    def call_from_console(self):
        return "[Command] Perintah hanya dapat digunakan di PSO2."


@CommandHandler("op", "[Hanya Admin] Tambah Admin.", True)
class OpCommand(Command):
    def call_from_client(self, client):
        if len(self.args.split(" ")) < 2:
            client.send_crypto_packet(
<<<<<<< HEAD
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %sop <SegaID>)" % config.globalConfig.get_key('commandPrefix'),
                                                  0x3).build())
=======
                packetFactory.SystemMessagePacket(
                    "[Proxy] {red}Invalid usage.\n(Usage: %sop <SegaID>)".format(
                        config.globalConfig['commandPrefix']
                    ),
                    0x3
                ).build()
            )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            return
        player = self.args.split(" ")[1]
        if not config.is_admin(player):
            current_admins = config.globalConfig['admins']
            current_admins.append(player)
            config.globalConfig.set_key('admins', current_admins)
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}%s Ditambahkan sebagai Admin." % player,
                                                  0x3).build())
        else:
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}%s Sudah menjadi Admin." % player, 0x3).build())

    def call_from_console(self):
        if len(self.args.split(" ")) < 2:
            return "[PCP Bot] Perintah salah!. (Contoh: op <SegaID>)"
        player = self.args.split(" ")[1]
        if not config.is_admin(player):
            current_admins = config.globalConfig['admins']
            current_admins.append(player)
            config.globalConfig.set_key('admins', current_admins)
            return "[PCP Bot] %s Ditambahkan sebagai Admin." % player
        else:
            return "[PCP Bot] %s Sudah menjadi Admin." % player


@CommandHandler("deop", "[Hanya Admin] Hapus Admin.", True)
class DeopCommand(Command):
    def call_from_client(self, client):
        if len(self.args.split(" ")) < 2:
            client.send_crypto_packet(
<<<<<<< HEAD
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %sdeop <SegaID>)" % config.globalConfig.get_key('commandPrefix'),
                                                  0x3).build())
=======
                packetFactory.SystemMessagePacket(
                    "[Proxy] {}Invalid usage.\n(Usage: {}deop <SegaID>)".format(
                        "{red}",
                        config.globalConfig['commandPrefix']
                    ),
                    0x3
                ).build()
            )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            return
        player = self.args.split(" ")[1]
        if config.is_admin(player):
            current_admins = config.globalConfig['admins']
            current_admins.remove(player)
            config.globalConfig.set_key('admins', current_admins)
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}%s Berhasil dihapus dari Admin." % player,
                                                  0x3).build())
        else:
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}%s Bukan Admin." % player, 0x3).build())

    def call_from_console(self):
        if len(self.args.split(" ")) < 2:
            return "[PCP Bot] Perintah salah!. (Contoh: deop <SegaID>"
        player = self.args.split(" ")[1]
        if not config.is_admin(player):
            current_admins = config.globalConfig['admins']
            current_admins.remove(player)
            config.globalConfig.set_key('admins', current_admins)
            return "[PCP Bot] %s Berhasil dihapus dari admin." % player
        else:
            return "[PCP Bot] %s Bukan Admin." % player


@CommandHandler("help", "Daftar Perintah.")
class HelpCommand(Command):
    def call_from_client(self, client):
        string = "=== Perintah PCP Network ===\n\n"
        user_command_count = 0
        for command, cData in sorted(commandList.iteritems()):
            if cData[1] is not None:
                if cData[2] is not None:
                    if not cData[2]:
                        user_command_count += 1
<<<<<<< HEAD
                        string += "%s%s - %s\n\n" % (config.globalConfig.get_key('commandPrefix'), command, cData[1])
                else:
                    user_command_count += 1
                    string += "%s%s - %s\n\n" % (config.globalConfig.get_key('commandPrefix'), command, cData[1])
        for command, cData in plugin_manager.commands.iteritems():
=======
                        string += "%s%s - %s\n\n" % (config.globalConfig['commandPrefix'], command, cData[1])
                else:
                    user_command_count += 1
                    string += "%s%s - %s\n\n" % (config.globalConfig['commandPrefix'], command, cData[1])
        for command, cData in sorted(plugin_manager.commands.iteritems()):
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            if cData[1] is not None:
                if cData[2] is not None:
                    if not cData[2]:
                        user_command_count += 1
<<<<<<< HEAD
                        string += "%s%s - %s\n\n" % (config.globalConfig.get_key('commandPrefix'), command, cData[1])
                else:
                    user_command_count += 1
                    string += "%s%s - %s\n\n" % (config.globalConfig.get_key('commandPrefix'), command, cData[1])
        string += "%sadhelp - [Hanya Admin] Perintah Admin PCP Network.\n\n" % config.globalConfig.get_key('commandPrefix') #i add this manually because don't know how to get specific command.
        string += "=== Total Perintah %i ===" % user_command_count
        client.send_crypto_packet(packetFactory.SystemMessagePacket(string, 0x2).build())

    def call_from_console(self):
        return "=== Perintah Users PCP Network ===\n -- %s\n -- %s\n=== Perintah Admin PCP Network ===" % ('\n -- '.join(commandList.keys()), '\n -- '.join(plugin_manager.commands.keys()))


@CommandHandler("adhelp", "[Hanya Admin] Daftar Perintah Admin PCP Network.", True)
class HelpCommandADM(Command):
    def call_from_client(self, client):
        string = "=== Perintah Admin PCP Network ===\n\n"
        user_command_count = 0
        for command, cData in commandList.iteritems():
=======
                        string += "%s%s - %s\n\n" % (config.globalConfig['commandPrefix'], command, cData[1])
                else:
                    user_command_count += 1
                    string += "%s%s - %s\n\n" % (config.globalConfig['commandPrefix'], command, cData[1])
        string += "{}suhelp - [Admin Only] Display proxy administrator command list.\n\n".format(
            config.globalConfig['commandPrefix']
        )
        # i add this manually because don't know how to get specific command.
        string += "=== %i commands in total ===" % user_command_count
        client.send_crypto_packet(packetFactory.SystemMessagePacket(string, 0x2).build())

    def call_from_console(self):
        return "=== PSO2Proxy Commands ===\n -- {}\n -- {}\n=== PSO2Proxy Commands ===".format(
            '\n -- '.join(commandList.keys()),
            '\n -- '.join(plugin_manager.commands.keys())
        )


@CommandHandler("suhelp", "[Admin Only] Display proxy administrator command list.", True)
class HelpCommandADM(Command):
    def call_from_client(self, client):
        string = "=== PSO2Proxy Commands ===\n"
        user_command_count = 0
        for command, cData in sorted(commandList.iteritems()):
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            if cData[1] is not None:
                if cData[2] is not None:
                    if cData[2]:
                        user_command_count += 1
<<<<<<< HEAD
                        string += "%s%s - %s\n\n" % (config.globalConfig.get_key('commandPrefix'), command, cData[1])
        for command, cData in plugin_manager.commands.iteritems():
=======
                        string += "%s%s - %s\n\n" % (config.globalConfig['commandPrefix'], command, cData[1])
        for command, cData in sorted(plugin_manager.commands.iteritems()):
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            if cData[1] is not None:
                if cData[2] is not None:
                    if cData[2]:
                        user_command_count += 1
<<<<<<< HEAD
                        string += "%s%s - %s\n\n" % (config.globalConfig.get_key('commandPrefix'), command, cData[1])
=======
                        string += "%s%s - %s\n\n" % (config.globalConfig['commandPrefix'], command, cData[1])
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
        string += "=== %i commands in total ===" % user_command_count
        client.send_crypto_packet(packetFactory.SystemMessagePacket(string, 0x2).build())


@CommandHandler("ol", "Total users terkoneksi.")
class CountCommand(Command):
    def call_from_client(self, client):
        string = '{yel}[PCP Bot] {gre}Users yang terkoneksi: {ora}%s{yel}.' % len(data.clients.connectedClients)
        client.send_crypto_packet(packetFactory.SystemMessagePacket(string, 0x3).build())

    def call_from_console(self):
        return "[PCP Bot] User yang terkoneksi: %s." % len(data.clients.connectedClients)


@CommandHandler("reloadbans")
class ReloadBans(Command):
    def call_from_console(self):
        return config.load_bans()


@CommandHandler("listbl", "[Hanya Admin] Daftar Blacklist.", True)
class ListBans(Command):
    def call_from_client(self, client):
        string = "=== Daftar Blacklist ===\n"
        for ban in config.banList:
            if 'segaId' in ban:
                string += "SEGA ID: %s " % ban['segaId']
            if 'playerId' in ban:
                string += "Player ID: %s" % ban['playerId']
            string += "\n"
        client.send_crypto_packet(packetFactory.SystemMessagePacket(string, 0x2).build())

    def call_from_console(self):
        output = ""
        for ban in config.banList:
            output += '[Blacklist] %s Diblacklist.\n' % str(ban)
        output += '[Blacklist] Total Blacklist: %i .' % len(config.banList)
        return output


@CommandHandler("bl", "[Hanya Admin] Blacklist Users.", True)
class Ban(Command):
    def call_from_client(self, client):
        args = self.args.split(' ')
        if len(args) < 3:
<<<<<<< HEAD
            client.send_crypto_packet(packetFactory.SystemMessagePacket(
                "{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %sbl segaid <SegaID>)" % config.globalConfig.get_key('commandPrefix'), 0x3).build())
=======
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket(
                    "[Command] {}Invalid usage.\n(Usage: {}ban <SegaID/PlayerID> <value>)".format(
                        "{red}",
                        config.globalConfig['commandPrefix']
                    ),
                    0x3
                ).build()
            )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            return
        if args[1] == "segaid":
            if config.is_segaid_banned(args[2]):
                client.send_crypto_packet(
                    packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}%s Sudah ada diBlacklist." % args[2], 0x3).build())
                return
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}%s Berhasil diBlacklist." % args[2], 0x3).build())
            config.banList.append({'segaId': args[2]})
            config.save_bans()
        elif args[1] == "pid":
            if config.is_player_id_banned(args[2]):
                client.send_crypto_packet(
                    packetFactory.SystemMessagePacket('{yel}[PCP Bot] {red}%s Sudah ada diBlacklist.' % args[2], 0x3).build())
                return
            config.banList.append({'playerId': args[2]})
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}%s Berhasil diBlacklist." % args[2], 0x3).build())
            config.save_bans()
        else:
            client.send_crypto_packet(packetFactory.SystemMessagePacket(
                "{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %sbl segaid <SegaID>)", 0x3).build())
            return

    def call_from_console(self):
        args = self.args.split(' ')
        if len(args) < 3:
            return "[PCP Bot] Perintah salah!.(Contoh: bl segaid <SegaID>)"
        if args[1] == "segaid":
            if config.is_segaid_banned(args[2]):
                return "[PCP Bot] %s Sudah ada diBlacklist." % args[2]
            config.banList.append({'segaId': args[2]})
            config.save_bans()
        elif args[1] == "pid":
            if config.is_player_id_banned(args[2]):
                return '[PCP Bot] %s Berhasil diBlacklist.' % args[2]
            config.banList.append({'playerId': args[2]})
            config.save_bans()
        else:
            return "[PCP Bot] Perintah salah!.(Contoh: bl segaid <SegaID User>)"


@CommandHandler("unbl", "[Hanya Admin] Hapus Blacklist users.", True)
class Unban(Command):
    def call_from_client(self, client):
        args = self.args.split(' ')
        if len(args) < 3:
<<<<<<< HEAD
            client.send_crypto_packet(packetFactory.SystemMessagePacket(
                "{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %sunbl segaid <SegaID User)" % config.globalConfig.get_key('commandPrefix'), 0x3).build())
=======
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket(
                    "[Command] {}Invalid usage.\n(Usage: {}unban <SegaID/PlayerID> <value>)".format(
                        "{red",
                        config.globalConfig['commandPrefix']
                    ),
                    0x3
                ).build()
            )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            return
        if args[1] == "segaid":
            if not config.is_segaid_banned(args[2]):
                client.send_crypto_packet(
                    packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}%s Tidak ada di Blacklist." % args[2], 0x3).build())
                return
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}%s Berhasil dihapus dari Blacklist." % args[2], 0x3).build())
            config.banList.remove({'segaId': args[2]})
            config.save_bans()
        elif args[1] == "pid":
            if not config.is_player_id_banned(args[2]):
                client.send_crypto_packet(
                    packetFactory.SystemMessagePacket('{yel}[PCP Bot] {red}%s Tidak ada di Blacklist.' % args[2], 0x3).build())
                return
            config.banList.remove({'playerId': (args[2])})
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}%s Berhasil dihapus dari Blacklist." % args[2], 0x3).build())
            config.save_bans()
        else:
<<<<<<< HEAD
            client.send_crypto_packet(packetFactory.SystemMessagePacket(
                "{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %sunbl segaid <SegaID User>)" % config.globalConfig.get_key('commandPrefix'), 0x3).build())
=======
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket(
                    "[Command] {red}Invalid usage. \n(Usage: %sunban <SegaID/PlayerID> <value>)".foramt(
                        config.globalConfig['commandPrefix']
                    ),
                    0x3
                ).build()
            )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            return

    def call_from_console(self):
        args = self.args.split(' ')
        if len(args) < 3:
            return "[PCP Bot] Perintah Salah!. (Contoh: unbl segaid <SegaID User>)"
        if args[1] == "segaid":
            if not config.is_segaid_banned(args[2]):
                return '[PCP Bot] %s Tidak ada di Blacklist.' % args[2]
            config.banList.remove({'segaId': args[2]})
            config.save_bans()
        elif args[1] == "pid":
            if not config.is_player_id_banned(args[2]):
                return '[PCP Bot] %s Tidak ada di Blacklist.' % args[2]
            config.banList.remove({'playerId': args[2]})
            config.save_bans()
        else:
            return "[PCP Bot] Perintah salah!. (Contoh: unbl segaid <SegaID User>)"


@CommandHandler("kick", "[Hanya Admin] Kick/DC Users dari Proxy.", True)
class Kick(Command):
    def call_from_client(self, client):
        args = self.args.split(' ')
        if len(args) < 2:
            client.send_crypto_packet(
<<<<<<< HEAD
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %skick <PlayerID>)" % config.globalConfig.get_key('commandPrefix'),
                                                  0x3).build())
=======
                packetFactory.SystemMessagePacket(
                    "[Command] {}Invalid usage.\n(Usage: {}kick <PlayerID>)".format(
                        "{red}",
                        config.globalConfig['commandPrefix']
                    ),
                    0x3
                ).build()
            )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            return
        if not args[1].isdigit():
            return "{yel}[PCP Bot] {red}%s Bukan PlayerID." % args[1]
        if int(args[1]) in data.clients.connectedClients:
            if data.clients.connectedClients[int(args[1])].get_handle() is not None:
                data.clients.connectedClients[int(args[1])].get_handle().send_crypto_packet(
                    packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}Anda dikick dari proxy oleh admin.",
                                                      0x2).build())
                data.clients.connectedClients[int(args[1])].get_handle().transport.loseConnection()
                client.send_crypto_packet(
                    packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}%s Berhasil diKick." % args[1], 0x3).build())
            else:
                return "{yel}[PCP Bot] {red}%s PlayerID tidak ditemukan." % args[1]
        else:
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}%s PlayerID tidak ditemukan." % args[1], 0x3).build())

    def call_from_console(self):
        args = self.args.split(' ')
        if len(args) < 2:
            return "[PCP Bot] Perintah Salah!. (Contoh: kick <PlayerID>)"
        if not args[1].isdigit():
            return "[PCP Bot] {red}%s Bukan PlayerID." % args[1]
        if int(args[1]) in data.clients.connectedClients:
            if data.clients.connectedClients[int(args[1])].get_handle() is not None:
                data.clients.connectedClients[int(args[1])].get_handle().send_crypto_packet(
<<<<<<< HEAD
                    packetFactory.SystemMessagePacket("[PCP Bot] Anda dikick dari proxy oleh admin.", 0x1).build())
=======
                    packetFactory.SystemMessagePacket(
                        "[Proxy] You have been disconnected from the proxy by an admin.",
                        0x1
                    ).build()
                )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
                data.clients.connectedClients[int(args[1])].get_handle().transport.loseConnection()
                return "[PCP Bot] %s Berhasil diKick." % args[1]
            else:
                return "[PCP Bot] %s PlayerID tidak ditemukan." % args[1]
        else:
            return "[PCP Bot] %s PlayerID tidak ditemukan." % args[1]


@CommandHandler("oldata", "[Hanya Admin] Data players yang online", True)
class ListClients(Command):
    def call_from_client(self, pclient):
        string = "=== Players yang online: %i === \n" % len(data.clients.connectedClients)
        for ip, client in data.clients.connectedClients.iteritems():
            client_handle = client.get_handle()
            if client_handle is None:
                continue
            client_host = client_handle.transport.getPeer().host
            client_segaid = client_handle.myUsername
            if client_segaid is None:
                continue
            client_segaid = client_segaid.rstrip('\0')
            client_player_id = client_handle.playerId
            if client_player_id in data.players.playerList:
                client_player_name = data.players.playerList[client_player_id][0].rstrip('\0')
            else:
                client_player_name = None
            client_ship = None
            client_block = None
            block_number = client_handle.transport.getHost().port
            if block_number in data.blocks.blockList:
                client_ship = data.clients.get_ship_from_port(block_number)
                client_block = data.blocks.blockList[block_number][1].rstrip('\0')
            string += "[%s]\n - IP: %s \n - SEGA ID: %s \n - Player ID: %s \n - Ship: %s \n - Block: %s \n \n" % (
                client_player_name, client_host, client_segaid, client_player_id, client_ship, client_block)
        pclient.send_crypto_packet(packetFactory.SystemMessagePacket(string, 0x2).build())

    def call_from_console(self):
        string = "=== Players yang online: %i === \n" % len(data.clients.connectedClients)
        for ip, client in data.clients.connectedClients.iteritems():
            client_handle = client.get_handle()
            if client_handle is None:
                continue
            client_host = client_handle.transport.getPeer().host
            client_segaid = client_handle.myUsername
            if client_segaid is None:
                continue
            client_segaid = client_segaid.rstrip('\0')
            client_player_id = client_handle.playerId
            if client_player_id in data.players.playerList:
                client_player_name = data.players.playerList[client_player_id][0].rstrip('\0')
            else:
                client_player_name = None
            client_ship = None
            client_block = None
            if isinstance(client_handle, ShipProxy):
                block_number = client_handle.transport.getHost().port
                if block_number in data.blocks.blockList:
                    client_ship = data.clients.get_ship_from_port(block_number)
                    client_block = data.blocks.blockList[block_number][1].rstrip('\0')
            string += "[%s]\n - IP: %s \n - SEGA ID: %s \n - Player ID: %s \n - Ship: %s \n - Block: %s \n \n" % (
                client_player_name, client_host, client_segaid, client_player_id, client_ship, client_block)
        return string
		
@CommandHandler("ollist", "List Player yang online.")
class ListClients(Command):
    def call_from_client(self, pclient):
        string = "=== Players yang online: %i === \n" % len(data.clients.connectedClients)
        for ip, client in data.clients.connectedClients.iteritems():
            client_handle = client.get_handle()
            if client_handle is None:
                continue
            client_host = client_handle.transport.getPeer().host
            client_segaid = client_handle.myUsername
            if client_segaid is None:
                continue
            client_segaid = client_segaid.rstrip('\0')
            client_player_id = client_handle.playerId
            if client_player_id in data.players.playerList:
                client_player_name = data.players.playerList[client_player_id][0].rstrip('\0')
            else:
                client_player_name = None
            client_ship = None
            client_block = None
            block_number = client_handle.transport.getHost().port
            if block_number in data.blocks.blockList:
                client_ship = data.clients.get_ship_from_port(block_number)
                client_block = data.blocks.blockList[block_number][1].rstrip('\0')
            string += "[Ship-%s : %s | %s] \n" % (
                client_ship, client_block[:5], client_player_name)
        pclient.send_crypto_packet(packetFactory.SystemMessagePacket(string, 0x2).build())

    def call_from_console(self):
        string = "=== Players yang online: %i === \n" % len(data.clients.connectedClients)
        for ip, client in data.clients.connectedClients.iteritems():
            client_handle = client.get_handle()
            if client_handle is None:
                continue
            client_host = client_handle.transport.getPeer().host
            client_segaid = client_handle.myUsername
            if client_segaid is None:
                continue
            client_segaid = client_segaid.rstrip('\0')
            client_player_id = client_handle.playerId
            if client_player_id in data.players.playerList:
                client_player_name = data.players.playerList[client_player_id][0].rstrip('\0')
            else:
                client_player_name = None
            client_ship = None
            client_block = None
            if isinstance(client_handle, ShipProxy):
                block_number = client_handle.transport.getHost().port
                if block_number in data.blocks.blockList:
                    client_ship = data.clients.get_ship_from_port(block_number)
                    client_block = data.blocks.blockList[block_number][1].rstrip('\0')
            string += "[``Ship-%s : %s `` | %s]\n" % (
                client_ship, client_block[:5], client_player_name)
        return string
		


@CommandHandler("bc", "[Hanya Admin] Broadcast ke semua users.", True)
class GlobalMessage(Command):
    def call_from_client(self, client):
        message = None
        print(self.args)
        if len(self.args.split(' ', 1)) < 2:
<<<<<<< HEAD
            client.send_crypto_packet(packetFactory.SystemMessagePacket("{yel}[PCP Bot] {red}Perintah salah!.\n{gre}(Contoh: %sbc  <pesan>)" % config.globalConfig.get_key('commandPrefix'), 0x3).build())
=======
            client.send_crypto_packet(
                packetFactory.SystemMessagePacket(
                    "[Command] {}Invalid usage.\n(Usage: {}globalmsg  <message>)".format(
                        "{red}",
                        config.globalConfig['commandPrefix']
                    ),
                    0x3
                ).build()
            )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
            return
        message = self.args.split(' ', 1)[1]
        for client in data.clients.connectedClients.values():
            if client.get_handle() is not None:
                client.get_handle().send_crypto_packet(
                    packetFactory.SystemMessagePacket("[PROXY-BROADCAST] %s" % message, 0x0).build())

    def call_from_console(self):
        message = None
        if len(self.args.split(' ', 1)) < 2:
            return "[PCP Bot] Perintah salah!. (Contoh: bc <pesan>)"
        try:
            mode = int(self.args.split(' ', 2)[1])
        except ValueError:
            mode = 0x0
            message = self.args.split(' ', 1)[1]

        if message is None:
            message = self.args.split(' ', 2)[2]
        SMPacket = packetFactory.SystemMessagePacket("[PROXY-BROADCAST] %s" % message, mode).build()
        for client in data.clients.connectedClients.values():
            if client.get_handle() is not None:
                client.get_handle().send_crypto_packet(SMPacket)
        return "[PCP Bot] Broadcast Terkirim!"


@CommandHandler("exit")
class Exit(Command):
    def call_from_console(self):
        reactor.callFromThread(reactor.stop)
        return "[ShipProxy] Stopping proxy server..."


@CommandHandler("reloadblocknames")
class ReloadBlockNames(Command):
    def call_from_console(self):
        return config.load_block_names()


@CommandHandler("reloadshiplabels")
class ReloadShipLables(Command):
    def call_from_console(self):
        return config.load_ship_names()


<<<<<<< HEAD
@CommandHandler("reloadplugin", "[Hanya Admin] Reload one plugin", True)
=======
profile = None


@CommandHandler("profile", "[Admin Only] Turn on profiling mode", True)
class Profiler(Command):
    def call_from_console(self):
        global profile
        if profile is None:
            profile = cProfile.Profile()
            profile.enable()
            SMPacket = packetFactory.SystemMessagePacket(
                "[Proxy Notice] Profiling mode has been enabled, expect lag while this runs.",
                0x0
            ).build()
            for client in data.clients.connectedClients.values():
                if client.get_handle() is not None:
                    client.get_handle().send_crypto_packet(SMPacket)
            return "[Profiling] Profiling has been enabled."
        else:
            profile.disable()
            out = open("profile_%s.txt" % calendar.timegm(datetime.datetime.utcnow().utctimetuple()), 'w')
            sort_by = 'cumulative'
            ps = pstats.Stats(profile, stream=out).sort_stats(sort_by)
            ps.print_stats()
            shutil.copy(out.name, "latest_profile.txt")
            out.close()
            profile = None
            SMPacket = packetFactory.SystemMessagePacket(
                "[Proxy Notice] Profiling mode has been disabled, any lag caused by this should subside.",
                0x0
            ).build()
            for client in data.clients.connectedClients.values():
                if client.get_handle() is not None:
                    client.get_handle().send_crypto_packet(SMPacket)
            return "[Profiling] Profiling has been disabled, results written to disk."


@CommandHandler("reloadplugin", "[Admin Only] Reload one plugin", True)
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
class ReloadPlugins(Command):
    def call_from_console(self):
        if len(self.args.split(' ')) < 2:
            return "[Command] Invalid usage. (Usage: reloadplugin <Plugin Name>)"
        modulearg = self.args.split(' ')[1]
        if modulearg not in sys.modules.keys():
            return "That plugin (%s) is not loaded." % modulearg
        output = "[ShipProxy] Reloading plugin: %s..." % modulearg
        rebuild.rebuild(sys.modules[modulearg])
        output += "[ShipProxy] Plugin reloaded!\n"
        return output


if useFaulthandler:
    @CommandHandler("dumptraceback", "[Hanya Admin] Dump stacktrack Proxy", True)
    class Fault(Command):
        def call_from_console(self):
            faulthandler.dump_traceback(file=open('log/tracestack.log', 'w+'), all_threads=True)
            return "[PCP Bot] dumpped state of Proxy"
