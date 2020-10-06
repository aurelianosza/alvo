import path
import sys

folder = path.Path(__file__).abspath()
sys.path.append(folder.parent.parent)

from interfaces import observer
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from multiprocessing import Process, Manager, Lock, Value
from ctypes import c_int

class SocketTCPController(observer.Observer):

    def __init__(self, strategy, name, port):
        super(SocketTCPController, self).__init__()
        self._connections = Manager().dict()

        self._thead = None
        self._mutex = Lock()

        self._name = name
        self._port = port

        self._strategy = strategy
        self._strategy.context = self

    def start(self):
        self._thead = Process(target=self.receiveConnections)
        self._thead.start()

    def join(self):
        self._thead.join()

    def update(self):
        val = self._strategy.execute()

        with self._mutex:
            for key, connection in self._connections.items():
                try:
                    connection.sendall(str(val).encode())
                except:
                    print("Error on {} client".format(key))
                    connection.close()
                    self._connections.pop(key)
                finally:
                    pass

    @staticmethod
    def generateName(addr):
        local, port = addr
        return "{}:{}".format(local, port)

    def receiveConnections(self):

        sock = socket(AF_INET, SOCK_STREAM)

        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        sock.bind(('0.0.0.0', self._port))

        sock.listen(0)

        print("Socket listen on\t {}".format(sock.getsockname()))

        while True:
            client, addr = sock.accept()

            print("{} Has connected".format(addr))

            with self._mutex:
                self._connections[SocketTCPController.generateName(addr)] = client

class SocketTCPOnceController(observer.Observer):

    def __init__(self, strategy, name, port):
        super(SocketTCPOnceController, self).__init__()

        self._val = Value(c_int, 0)

        self._name = name
        self._port = port

        self._thread = None
        self._mutex = Lock()

        self._strategy = strategy
        self._strategy.context = self

    def update(self):
        self._val.value = self._strategy.execute()

    def start(self):
        self._thread = Process(target=self.recvRequest)
        self._thread.start()

    def recvRequest(self):

        sock = socket(AF_INET, SOCK_STREAM)

        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        sock.bind(('0.0.0.0', self._port))

        sock.listen(0)

        print("Socket once listen on\t {}".format(sock.getsockname()))

        while True:
            client, addr = sock.accept()

            with self._mutex:
                client.sendall(str(self._val.value).encode())

            client.close()


if __name__ == '__main__':

    from strategies.temperaturaStrategy import TemperaturaStrategy
    from models import medidor

    m = medidor.Medidor()

    s = SocketTCPController(TemperaturaStrategy(), 'temperatura', 7555)

    m.attach(s)

    m.start()

    s.start()
    s.join()




