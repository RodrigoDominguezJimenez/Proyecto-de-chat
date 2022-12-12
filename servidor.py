import socket
import threading
import json

class Servidor:
    """docstring for Servidor."""
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clientes = list()
        self.nicknames = list()
        self.startServer()

    def startServer(self):
        """
        Se inicializa el servidor y por cada cliente que se conecta
        se crea un hilo
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        print("Servidor escuchando en %s:%s" % (self.ip, self.port))
        while True:
            cltConn, cltAddr = self.socket.accept()
            print("Cliente conectado de", cltAddr)
            hilo_cliente = threading.Thread(target=self.clientHandle, args=(cltConn, ))
            hilo_cliente.setDaemon(True)
            hilo_cliente.start()

    def clientHandle(self, clientConnection):
        """
        Manejo de clientes, los clientes pueden enviar 3 tipos de mensajes
        handshake, broadcast y direct
        """
        index = None
        connected = False
        nName = None
        fname = None
        while True:
            try:
                data = clientConnection.recv(1024).decode()
                if not data:
                    break
                jsonObj = json.loads(data)
                if jsonObj["type"] == "handshake":
                    if jsonObj['nickname'] not in self.nicknames:
                        self.clientes.append(clientConnection)
                        # Responder con la lista de clientes
                        jsonMsg = json.dumps({
                            "type": "list_clients",
                            "clients": self.nicknames
                        })
                        clientConnection.send(jsonMsg.encode())
                        nName = jsonObj['nickname']
                        self.nicknames.append(nName)
                        index = self.clientes.index(clientConnection)
                        # Avisar a los otros clientes que el usuario se ha conectado
                        jsonMsg = json.dumps({
                            "type": "conn_notif",
                            "nickname": jsonObj['nickname']
                        })
                        self.sendBroadcast(index, jsonMsg, False)
                        connected = True
                    else:
                        jsonMsg = json.dumps({
                            "type": "nick_err"
                        })
                        clientConnection.send(jsonMsg.encode())
                        connected = False
                        break
                elif jsonObj["type"] == "broadcast":
                    # Enviar un mensaje de broadcast
                    index = self.clientes.index(clientConnection)
                    jsonMsg = json.dumps({
                        "type": "broadcast",
                        "from": self.nicknames[index],
                        "msg": jsonObj["msg"]
                    })
                    self.sendBroadcast(index, jsonMsg, False)
                elif jsonObj["type"] == "direct":
                    # Mensajes directos entre clientes
                    index = self.clientes.index(clientConnection)
                    jsonMsg = json.dumps({
                        "type": "direct",
                        "from": self.nicknames[index],
                        "msg": jsonObj["msg"]
                    })
                    receiver_index = self.nicknames.index(jsonObj["to"])
                    self.sendDirect(receiver_index, jsonMsg, False)
            except Exception as e:
                raise
        if connected:
            jsonMsg = json.dumps({
                "type": "dis_notif",
                "nickname": nName
            })
            self.clientes.remove(clientConnection)
            for cliente in self.clientes:
                try:
                    cliente.send(jsonMsg.encode())
                except Exception as e:
                    raise
            self.nicknames.remove(nName)
        print("Cliente desconectado", clientConnection.getpeername())
        clientConnection.close()

    def sendBroadcast(self, senderIndex, msg, file):
        """
        Obtiene la lista de clientes (excepto el que envia el mensaje) y
        envia el mensaje a cada uno de los clientes
        """
        recipients = self.clientes[:senderIndex] + self.clientes[senderIndex+1:]
        if recipients:
            for cliente in recipients:
                try:
                    if(file):
                        cliente.send(msg)
                    else:
                        cliente.send(msg.encode())
                except Exception as e:
                    raise

    def sendDirect(self, receiverIndex, msg, file):
        """
        Envia un mensaje a un cliente especifico
        """
        cliente = self.clientes[receiverIndex]
        if file:
            cliente.send(msg)
        else:
            cliente.send(msg.encode())

if __name__ == '__main__':
    ip = "0.0.0.0"
    port = 8500
    s = Servidor(ip, port)
