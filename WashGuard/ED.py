import sys
import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from init import *
from MQTT_client import *

# Creating Client name -
global clientname
r=random.randrange(1,10000000)
clientname="ED_sensor-"+Machine_ID+"-"+str(r)
update_rate = 5000 # in msec


class ConnectionDock(QDockWidget):
    """Main """

    def __init__ (self, mc):
        QDockWidget.__init__(self)

        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        global clientname
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(ED_topic)

        self.ElectricCurrent = QLineEdit()
        self.ElectricCurrent.setText('')

        self.DrumRotation = QLineEdit()
        self.DrumRotation.setText('')

        formLayot = QFormLayout()
        formLayot.addRow("Turn On/Off", self.eConnectbtn)
        formLayot.addRow("Pub topic", self.ePublisherTopic)
        formLayot.addRow("ElectricCurrent", self.ElectricCurrent)
        formLayot.addRow("DrumRotation", self.DrumRotation)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Connect")

    def on_connected (self):
        self.eConnectbtn.setStyleSheet("background-color: green")

    def on_button_connect_click (self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()

    def push_button_click (self):
        self.mc.publish_to(self.ePublisherTopic.text(), '"value":1')


class MainWindow(QMainWindow):

    def __init__ (self, parent=None):
        QMainWindow.__init__(self, parent)

        # Init of Mqtt_client class
        self.mc = Mqtt_client()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(update_rate)  # in msec

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 600, 300, 150)
        self.setWindowTitle('ED')

        # Init QDockWidget objects
        self.connectionDock = ConnectionDock(self.mc)

        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)

    def update_data (self):
        print('Next update')
        Electric =  2 +  random.randrange(5, 25)
        DrumRotation = 300 + random.randrange(50, 1600)
        current_data = 'ElectricCurrent: ' + str(Electric) + ' DrumRotation: ' + str(DrumRotation)
        self.connectionDock.ElectricCurrent.setText(str(Electric)+ ' amp')
        self.connectionDock.DrumRotation.setText(str(DrumRotation)+' rpm')
        self.mc.publish_to(ED_topic, current_data)

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()