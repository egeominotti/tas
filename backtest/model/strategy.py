from abc import ABCMeta, abstractmethod


class Strategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def add_strategy(self, func):
        raise NotImplementedError("Should implement generate_signals()!")
