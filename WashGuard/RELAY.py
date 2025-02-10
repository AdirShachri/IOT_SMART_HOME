import sys
import random
from time import sleep

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from init import *
from MQTT_client import *

# Creating Client name - should be unique
global clientname
r = random.randrange(1, 10000000)
clientname = "RELAY_sensor-Id234" + str(r)
global ON
ON = False


class MC(Mqtt_client):
    def __init__(self):
        super().__init__()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        ic(f"Received message on topic '{topic}': {m_decode}")
        if "running" in m_decode or "stop" in m_decode:
            try:
                mainwin.connectionDock.update_btn_state(m_decode)
            except Exception as e:
                ic(f"Failed to update button state: {e}")


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



        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText(relay_topic)

        self.ePushtbtn = QPushButton("", self)
        self.ePushtbtn.setToolTip("Push me")
        self.ePushtbtn.setStyleSheet("background-color: gray")

        formLayot = QFormLayout()
        formLayot.addRow("Turn On/Off", self.eConnectbtn)
        formLayot.addRow("Sub topic", self.eSubscribeTopic)
        formLayot.addRow("Machine Status", self.ePushtbtn)

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
        sleep(0.1)
        self.mc.subscribe_to(self.eSubscribeTopic.text())

    def update_btn_state(self, text):
        global ON
        if not ON and "running" in text:
            self.ePushtbtn.setStyleSheet("background-color: green")
            self.ePushtbtn.setText("Open")
            ON = True
        elif ON and "stop" in text:
            self.ePushtbtn.setStyleSheet("background-color: red")
            self.ePushtbtn.setText("Close")
            ON = False
        else:
            ic(f"Unexpected message received: {text}") 



class MainWindow(QMainWindow):

    def __init__ (self, parent=None):
        QMainWindow.__init__(self, parent)

        # Init of Mqtt_client class
        self.mc = MC()

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 300, 300, 150)
        self.setWindowTitle('RELAY')

        # Init QDockWidget objects
        self.connectionDock = ConnectionDock(self.mc)

        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
