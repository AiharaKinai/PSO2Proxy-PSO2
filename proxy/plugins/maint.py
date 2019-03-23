import commands
import packetFactory
from packetFactory import SystemMessagePacket
import plugins
maintmode = False


@plugins.CommandHook("maint", "[Hanya Admin] Proxy maintenance mode", True)
class maintmode(commands.Command):
    def call_from_client(self, client):
        global maintmode
        maintmode = not maintmode
        if maintmode:
            client.send_crypto_packet(packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}Maintenance mode: {ora}ON{gre}.", 0x3).build())
            return
        else:
            client.send_crypto_packet(packetFactory.SystemMessagePacket("{yel}[PCP Bot] {gre}Maintenance mode: {ora}OFF{gre}.", 0x3).build())
            return

    def call_from_console(self):
        global maintmode
        maintmode = not maintmode
        if maintmode:
            return "[PCP Bot] Maintenance mode: ON."
        else:
            return "[PCP Bot] Maintenance mode: OFF."


@plugins.PacketHook(0x11, 0x0)
def Maint_check(context, data):
    """

    :type context: ShipProxy.ShipProxy
    """
    global maintmode
    if not maintmode:
        return data
<<<<<<< HEAD
    context.send_crypto_packet(SystemMessagePacket("Proxy Lagi Maintenance. Silahkan coba beberapa saat lagi.", 0x1).build())
=======
    context.send_crypto_packet(
        SystemMessagePacket(
            "The PSO2 or PSO2Proxy server is currently undergoing maintenance. Please try again later.", 0x1
        ).build()
    )
>>>>>>> d4a7bf2cacdd48a2cfb02935e664e0f093252d00
    context.transport.loseConnection()
    return data
