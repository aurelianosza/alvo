import path
import sys

folder = path.Path(__file__).abspath()
sys.path.append(folder.parent.parent)

from interfaces import strategy


class TemperaturaStrategy(strategy.Strategy):

    def __init__(self):
        super(TemperaturaStrategy, self).__init__()

    def execute(self):
        return self.context.subject.temperatura
