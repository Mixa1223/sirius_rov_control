import time
from PyQt6.QtGui import QPixmap
from PySide6.QtCore import Qt

from camera import Worker1
from interface_code import *
import sys


class interface_custom(Ui_MainWindow):
    # Класс-наследник окна, создаваемого qt designer.
    # Использовать для любых изменений класса-родителя.

    # функции для работы с камерой
    def ImageUpdateSlot(self, Image):
        self.camera_feed.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()

    def exit(self):
        sys.exit(0)
    '''
    def minimizeWindow(self, MainWindow):
        MainWindow.showMinimized()

    def maximizeWindow(self, MainWindow):
        MainWindow.showMaximized()
        self.btn_maximize.hide()
        self.btn_restore.show()

    def restoreWindow(self, MainWindow):
        MainWindow.showNormal()
        self.btn_restore.hide()
        self.btn_maximize.show()
'''
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.btn_close.clicked.connect(self.exit)
        '''
        self.btn_restore.hide()
        self.btnCameraTab.clicked.connect(self.SwitchTabCamera)
        self.btnDebugTab.clicked.connect(self.SwitchTabDebug)
        self.btn_minimize.clicked.connect(lambda: self.minimizeWindow(MainWindow))
        self.btn_maximize.clicked.connect(lambda: self.maximizeWindow(MainWindow))
        self.btn_restore.clicked.connect(lambda: self.restoreWindow(MainWindow))
        '''
        # окно без рамки
        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)

    def updateUI(self, state):
        if state:

            if state.Gamepad.wButtons & 0b1000000000000000:  # треугольник\Y - поднять робота вверх
                self.buttonA_perc.setText("0%")
                self.buttonY_perc.setText("100%")
            elif state.Gamepad.wButtons & 0b0001000000000000:  # крестик\A - погрузить робота
                self.buttonY_perc.setText("0%")
                self.buttonA_perc.setText("100%")
            else:
                self.buttonY_perc.setText("0%")
                self.buttonA_perc.setText("0%")

            if state.Gamepad.wButtons & 0b100000000000000:  # квадрат\Х - открыть манипулятор
                self.buttonB_perc.setText("0%")
                time.sleep(0.005)
                self.buttonX_perc.setText("100%")
            elif state.Gamepad.wButtons & 0b10000000000000:  # круг\В - закрыть манипулятор
                self.buttonX_perc.setText("0%")
                time.sleep(0.005)
                self.buttonB_perc.setText("100%")
            else:
                self.buttonX_perc.setText("0%")
                self.buttonB_perc.setText("0%")

            if state.Gamepad.wButtons & 0b0000001000000000:  # R1\RB - поворот вокруг своей оси по часовой стрелке
                self.buttonRB_perc.setText("100%")
            else:
                self.buttonRB_perc.setText("0%")

            if state.Gamepad.wButtons & 0b0000000100000000:  # L1\LB - поворот вокруг своей оси против часовой стрелки
                self.buttonLB_perc.setText("100%")
            else:
                self.buttonLB_perc.setText("0%")

            self.buttonLT_perc.setText(str(int((state.Gamepad.bLeftTrigger/255)*100))+"%")
            self.buttonRT_perc.setText(str(int((state.Gamepad.bRightTrigger / 255) * 100)) + "%")

    def debug_updatePacketUI(self, rov_UDP):
        time.sleep(0.02)  # задержка 20 мс
        self.thrus_vert_0_perc.setText(str(rov_UDP.toWrite[0]))
        self.thrus_vert_1_perc.setText(str(rov_UDP.toWrite[1]))
        time.sleep(0.001)
        self.thrus_horiz_0_perc.setText(str(rov_UDP.toWrite[2]))
        time.sleep(0.001)
        self.thrus_horiz_1_perc.setText(str(rov_UDP.toWrite[3]))
        time.sleep(0.001)
        self.thrus_horiz_2_perc.setText(str(rov_UDP.toWrite[4]))
        time.sleep(0.001)
        self.thrus_horiz_3_perc.setText(str(rov_UDP.toWrite[5]))
        time.sleep(0.001)
        self.manip_rotation_perc.setText(str(rov_UDP.toWrite[6]))
        time.sleep(0.001)
        self.manip_grabber_perc.setText(str(rov_UDP.toWrite[7]))
        time.sleep(0.001)
