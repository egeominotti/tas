from abc import ABCMeta, abstractmethod


class Strategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError("Should implement generate_signals()!")


class Portfolio(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def check_entry(self, func_stop_loss, func_take_profit):
        raise NotImplementedError("Should implement generate_signals()!")
