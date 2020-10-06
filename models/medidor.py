import path
import sys

folder = path.Path(__file__).abspath()
sys.path.append(folder.parent.parent)

from interfaces import observer
from time import sleep
from random import randint
from multiprocessing import Process, Queue

class Medidor(observer.Subject):

    def __init__(self):
        super(Medidor, self).__init__()
        self._temperatura = 0
        self._pressao = 0
        self._process_1 = None
        self._process_2 = None
        self._process_updating = None
        self._queue_1 = Queue()
        self._queue_2 = Queue()

    @property
    def temperatura(self):
        return self._temperatura

    @property
    def pressao(self):
        return self._pressao
        
    def start(self):
        self._process_1 = Process(target=self.updatePressao, args=(self._queue_1,)).start()
        self._process_2 = Process(target=self.updateTemperatura, args=(self._queue_2,)).start()
        self._process_updating = Process(target=self.update).start()

    def stop(self):
        self._process_1.terminate()
        self._process_2.terminate()
        self._process_updating.terminate()

    def update(self):
        while True :
            if not self._queue_1.empty():
                self._pressao = self._queue_1.get()
                self.notify()
            elif not self._queue_2.empty():
                self._temperatura = self._queue_2.get()
                self.notify()


    def updateTemperatura(self, queue):
        while True:
            sleep(randint(1, 120))
            queue.put(randint(-20, 45))

    def updatePressao(self, queue):
        while True:
            sleep(randint(1, 120))
            queue.put(randint(0, 999))

    def notify(self):
        for o in self.observers:
            o.update()
    

if __name__ == '__main__':

    class Sensor(observer.Observer):

        def __init__(self):
            super(Sensor, self).__init__()
            self._pressao = 0
            self._temperatura = 0

        def update(self):
            self._pressao = self.subject.pressao
            self._temperatura = self.subject.temperatura
            self.show()
            
        def show(self):
            print(" - Temperatura:\t{}\n - Pressao:\t{}\n".format(self._temperatura, self._pressao))

        
    s = Sensor()

    m = Medidor()

    m.attach(s)

    m.start()
