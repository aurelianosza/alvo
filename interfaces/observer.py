from abc import ABC, abstractmethod

class Subject(ABC):

    def __init__(self):
        # @var array
        self._observers = [] 

    @property
    def observers(self):
        return self._observers

    def attach(self, observer):
        self.observers.append(observer)
        observer.bind(self)

    def detach(self, observer):
        self.observers.remove(observer)
        observer.unbind()

    @abstractmethod
    def notify(self):
        raise Exception('Not implemented notify method')

class Observer(ABC):

    def __init__(self):
        self._subject = None

    def bind(self, subject):
        self._subject = subject

    def unbind(self):
        self._subject = None

    @property
    def subject(self):
        return self._subject

    @abstractmethod
    def update(self):
        raise Exception('Not implemented update method')




if __name__ == '__main__':

    class Sensor(Subject):

        def __init__(self):
            super(Sensor, self).__init__()
            self._integer = 0

        @property
        def integer(self):
            return self._integer

        @integer.setter
        def integer(self, integer):
            self._integer = integer
            self.notify()

        def notify(self):
            for observer in self.observers:
                observer.update()

    class Monitor(Observer):
        
        def __init__(self, name):
            super(Monitor, self).__init__()
            self._name = name

        def update(self):
            print('The {} has {} value'.format(self._name, self.subject.integer))




    subject = Sensor()

    monitor = Monitor("monitor 1")
    monitor2 = Monitor("monitor 2")

    subject.attach(monitor)
    subject.attach(monitor2)

    subject.integer = 100
    subject.integer = 50








