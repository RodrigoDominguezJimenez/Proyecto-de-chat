# Importar bibliotecas
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QToolBar,
QTabWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit,
QMenuBar, QAction, QDialog, QFormLayout, QSpinBox, QListWidget, QMessageBox,
QFileDialog)
from PyQt5.QtCore import QRegExp, pyqtSignal, QObject, QThread, Qt
from PyQt5.QtGui import QRegExpValidator, QIntValidator
import socket
import threading
import json
import sys
import os

#Sub-clase que hereda de QMainWindow
class VentanaPrincipal(QMainWindow):
    #constructor
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Le chat")
        mainLayout = QVBoxLayout()

        #Layout con el TabWidget y el ListWidget
        firstLayout = QHBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setObjectName("chat")
        self.tabs.addTab(textEdit, 'chat')
        self.tabs.currentWidget().acceptRichText = True
        self.tabs.currentWidget().document().setDefaultStyleSheet(".msg-send{background: #2ecc71;}.msg-receive{background: #3498db;}")
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        firstLayout.addWidget(self.tabs, 80)
        self.listClients = QListWidget()
        self.listClients.itemDoubleClicked.connect(self.selectClient)
        firstLayout.addWidget(self.listClients, 20)

        #Layout con el textedit y el button
        secondLayout = QHBoxLayout()
        self.textLine = QLineEdit()
        self.sendBtn = QPushButton()
        self.sendBtn.setText("Enviar")
        self.sendBtn.clicked.connect(self.sendText)
        secondLayout.addWidget(self.textLine)
        secondLayout.addWidget(self.sendBtn)

        # mainLayout.addWidget(self.tabs)
        mainLayout.addLayout(firstLayout)
        mainLayout.addLayout(secondLayout)
        contenedor = QWidget()
        contenedor.setLayout(mainLayout)

        settings_action = QAction("Server", self)
        settings_action.triggered.connect(self.serverSettingsDialog)

        menu_bar = QMenuBar()
        settings_menu = menu_bar.addMenu('&Settings')
        settings_menu.addAction(settings_action)
        self.setMenuBar(menu_bar)
        self.setCentralWidget(contenedor)

    def serverSettingsDialog(self):
        dlg = CustomDialog()
        dlg.exec_()
        if(dlg.connect):
            self.connetServer(dlg.ip, dlg.port, dlg.nickname)

    def sendText(self):
        index = self.tabs.currentIndex()
        receiver = self.tabs.tabText(index)
        msg = self.textLine.text()
        self.textLine.clear()
        if receiver == 'chat':
            jsonMsg = json.dumps({
                "type": "broadcast",
                "msg": msg
            })
        else:
            jsonMsg = json.dumps({
                "type": "direct",
                "to": receiver,
                "msg": msg
            })
        self.tabs.currentWidget().textCursor().insertBlock();
        self.socket.send(jsonMsg.encode())
        self.tabs.currentWidget().textCursor().insertHtml("<div>Tú: {}</div>".format(msg));

    def connetServer(self, serverIP, serverPort, nickname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((serverIP, serverPort))
        except Exception as e:
            sys.exit(1)
        #Enviar saludo (y nickname) al server
        self.sendHandshake(nickname)
        #Iniciar hilo para recibier mensajes
        self.running = True
        self.recvThread = RecvMsg(self.socket)
        self.recvThread.start()
        self.recvThread.recvclientlist.connect(self.handleClientList)
        self.recvThread.recvnotif.connect(self.handleNotif)
        self.recvThread.recvbroadcast.connect(self.handleBroadcast)
        self.recvThread.recvdirect.connect(self.handleDirect)

    def handleClientList(self, jsonObj):
        self.tabs.currentWidget().textCursor().insertBlock();
        self.tabs.currentWidget().textCursor().insertHtml("<div>Te has conectado a el chat</div>");
        self.listClients.addItem("Tú")
        self.listClients.addItems(jsonObj["clients"])

    def handleNotif(self, jsonObj):
        tab = self.tabs.findChild(QWidget, 'chat')
        self.tabs.setCurrentWidget(tab)
        if jsonObj["type"] == "conn_notif":
            self.tabs.currentWidget().textCursor().insertBlock();
            self.tabs.currentWidget().textCursor().insertHtml("<div>{} se ha conectado</div>".format(jsonObj["nickname"]));
            self.listClients.addItem(jsonObj["nickname"])
        else:
            self.tabs.currentWidget().textCursor().insertBlock();
            self.tabs.currentWidget().textCursor().insertHtml("<div>{} se ha desconectado</div>".format(jsonObj["nickname"]));
            itemlist = self.listClients.findItems(jsonObj["nickname"], Qt.MatchExactly)
            self.listClients.takeItem(self.listClients.row(itemlist[0]))

    def handleBroadcast(self, jsonObj):
        tab = self.tabs.findChild(QWidget, 'chat')
        self.tabs.setCurrentWidget(tab)
        if jsonObj["type"] == "file":
            self.tabs.currentWidget().textCursor().insertBlock()
            self.tabs.currentWidget().textCursor().insertHtml("<div>{} ha enviado el archivo: {}</div>".format(jsonObj["from"], jsonObj["msg"]));
        else:
            self.tabs.currentWidget().textCursor().insertBlock()
            self.tabs.currentWidget().textCursor().insertHtml("<div>{}: {}</div>".format(jsonObj["from"], jsonObj["msg"]));

    def handleDirect(self, jsonObj):
        tab = self.tabs.findChild(QWidget, jsonObj["from"])
        if tab is None:
            textEdit = QTextEdit()
            textEdit.setReadOnly(True)
            textEdit.setObjectName(jsonObj["from"])
            self.tabs.addTab(textEdit, jsonObj["from"])
            self.tabs.setCurrentWidget(textEdit)
        else:
            self.tabs.addTab(tab, jsonObj["from"])
            self.tabs.setCurrentWidget(tab)
        self.tabs.currentWidget().textCursor().insertBlock();
        if jsonObj["type"] == "file":
            self.tabs.currentWidget().textCursor().insertHtml("<div>{} te ha enviado el archivo: {}</div>".format(jsonObj["from"], jsonObj["msg"]));
        else:
            self.tabs.currentWidget().textCursor().insertHtml("<div>{}: {}</div>".format(jsonObj["from"], jsonObj["msg"]));

    def sendHandshake(self, nickname):
        msg = json.dumps({"type": "handshake","nickname": nickname})
        self.socket.send(msg.encode())

    def closeEvent(self, event):
        if(hasattr(self, 'socket')):
            self.socket.shutdown(socket.SHUT_RDWR)

    def selectClient(self, index):
        textEdit = QTextEdit()
        textEdit.setObjectName(index.text())
        self.tabs.addTab(textEdit, index.text())

    def closeTab(self, index):
        if index != 0:
            w = self.tabs.widget(index)
            self.tabs.removeTab(index)

class RecvMsg(QThread):
    recvclientlist = pyqtSignal(object)
    recvnotif = pyqtSignal(object)
    recvbroadcast = pyqtSignal(object)
    recvdirect = pyqtSignal(object)
    recvfile = pyqtSignal(object)
    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        while True:
            try:
                data = self.socket.recv(1024)
                print(data)
                if not data:
                    break
                jsonObj = json.loads(data)
                if jsonObj["type"] == "nick_err":
                    QMessageBox.warning(None, "Error de nickname", "El nickname elegido ya está en uso. Intente con otro")
                elif jsonObj["type"] == "list_clients":
                    self.recvclientlist.emit(jsonObj)
                elif jsonObj["type"] == "conn_notif":
                    self.recvnotif.emit(jsonObj)
                elif jsonObj["type"] == "dis_notif":
                    self.recvnotif.emit(jsonObj)
                elif jsonObj["type"] == "broadcast":
                    self.recvbroadcast.emit(jsonObj)
                elif jsonObj["type"] == "direct":
                    self.recvdirect.emit(jsonObj)
            except Exception as e:
                raise

class CustomDialog(QDialog):
    def __init__(self):
        self.connect = False
        super().__init__()
        self.setWindowTitle('Custom dialog')

        self.nicknameEdit = QLineEdit()
        self.nicknameEdit.textChanged.connect(self.checkNotEmpty)

        self.serverIPEdit = QLineEdit()
        self.serverIPEdit.textChanged.connect(self.checkNotEmpty)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.serverIPEdit.setValidator(ipValidator)

        self.serverPortSpin = QSpinBox()
        self.serverPortSpin.setMinimum(8000)
        self.serverPortSpin.setMaximum(10000)

        self.connectButton = QPushButton('Connect to server')
        self.connectButton.setEnabled(False)
        self.connectButton.clicked.connect(self.connetServer)

        layout = QFormLayout()
        layout.addRow('Nickname', self.nicknameEdit)
        layout.addRow('Sever IP', self.serverIPEdit)
        layout.addRow('Sever Port', self.serverPortSpin)
        layout.addRow(self.connectButton)
        self.setLayout(layout)

    def checkNotEmpty(self, txt):
        if not self.nicknameEdit.text() or not self.serverIPEdit.text() or not self.serverIPEdit.hasAcceptableInput():
            self.connectButton.setEnabled(False)
        else:
            self.connectButton.setEnabled(True)

    def connetServer(self):
        self.nickname = self.nicknameEdit.text()
        self.ip = self.serverIPEdit.text()
        self.port = self.serverPortSpin.value()
        self.connect = True
        self.close()

if __name__ == '__main__':
    # Instancia de la clase QApplication
    app = QApplication([])
    ventana = VentanaPrincipal()
    # Las ventanas se crean ocultas
    ventana.show()
    # Iniciar el ciclo de eventos
    app.exec_()
