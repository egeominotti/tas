from abc import ABCMeta, abstractmethod


class Strategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError("Should implement generate_signals()!")

    @abstractmethod
    def computed_data(self):
        raise NotImplementedError("Should implement generate_signals()!")
