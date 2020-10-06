from abc import ABC, abstractmethod

class Strategy(ABC):

    def __init__(self):
        self._context = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def execute(self):
        raise Exception("Method not implemented")


if __name__ == '__main__':

    import time
    import random
    from multiprocessing import Process


    class Sensor(object):

        def __init__(self, strategy):
            self._strategy = strategy
            self._integer = 0
            self._strategy.context = self
            self._process = None

        @property
        def integer(self):
            return self._integer

        @integer.setter
        def integer(self, integer):
            self._integer = integer
            print("Has arrived a new value {}".format(self._integer))

        def strategy(self, strategy):
            if strategy is None:
                return

            self._strategy = strategy
            self._strategy.context = self
    
        strategy = property(None, strategy)

        def start(self):
            if self._strategy is None:
                return

            self._process = Process(target=self._strategy.execute)
            self._process.start()

        def stop(self):
            if self._strategy is None:
                return

            self._strategy.stop()
            self._process.terminate()

    class LoopStrategy(Strategy):
        
        def __init__(self, interval):
            super(LoopStrategy, self).__init__()
            self._interval = interval
            self._busy = True

        def execute(self):
            while self._busy:
                time.sleep(self._interval)
                self.context.integer = random.randint(0, 99)

        def stop(self):
            print("finished")

    
    l1 = LoopStrategy(5)

    l2 = LoopStrategy(0.1)

    s = Sensor(l1)

    s.start()

    time.sleep(10)

    s.stop()

    s.strategy = l2

    s.start()

    time.sleep(10)

    s.stop()

    







    



        

        
