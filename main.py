import interface_custom
from interface_code import *
from threading import Thread
import connectivity
import XInput
import sys

def inputHandling():
    rov_UDP.sendPacket()
    while True:
        if XInput.get_connected()[0]:
            state = XInput.get_state(0)
            window.updateUI(state)
            if state:
                rov_UDP.formPacket(state)
                rov_UDP.sendPacket()
                #rov_UDP.receivePacket()
                window.debug_updatePacketUI(rov_UDP)
                rov_UDP.clearPacket()
        else:
            is_connected = XInput.get_connected()[0]
            while is_connected is False:
                is_connected = XInput.get_connected()[0]
                rov_UDP.sendPacket()
                #rov_UDP.receivePacket()
                window.debug_updatePacketUI(rov_UDP)
                rov_UDP.clearPacket()


if __name__ == "__main__":
    # прикрутить ввод ip адреса и порта
    rov_UDP = connectivity.UDP("192.168.0.177", 8080)
    # rov_UDP = UDP.UDPConnection("127.0.0.1", 8080) # local debug

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    window = interface_custom.interface_custom()
    window.setupUi(mainWindow)
    mainWindow.show()
    inputStream = Thread(target=inputHandling, args=(), daemon=True)
    inputStream.start()
    sys.exit(app.exec())