import path
import sys

folder = path.Path(__file__).abspath()
sys.path.append(folder.parent.parent)

from interfaces import strategy


class PressaoStrategy(strategy.Strategy):

    def __init__(self):
        super(PressaoStrategy, self).__init__()

    def execute(self):
        return self.context.subject.pressao
