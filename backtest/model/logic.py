from abc import ABCMeta, abstractmethod


class Logic(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def logic_signals(self, item) -> bool:
        raise NotImplementedError("Should implement generate_signals()!")


class LogicStopLoss(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def logic_check_stop_loss(self):
        raise NotImplementedError("Should implement generate_signals()!")


class LogicTakeProfit(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def logic_check_take_profit(self):
        raise NotImplementedError("Should implement generate_signals()!")
