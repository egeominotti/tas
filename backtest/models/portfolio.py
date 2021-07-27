from abc import ABCMeta, abstractmethod


class Portfolio(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def check_entry(self):
        raise NotImplementedError("Should implement generate_signals()!")
