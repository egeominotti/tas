from abc import ABCMeta, abstractmethod


class Portfolio(object):
    """
    Una classe base astratta che rappresenta un portfolio di
    posizioni (inclusi strumenti e contanti), determinate
    sulla base di una serie di segnali forniti da una Strategy
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_positions(self):
        """
        Fornisce la logica per determinare come le posizioni del
        portafoglio sono allocate sulla base dei segnali
        previsionali e dei contanti disponibili
        """
        raise NotImplementedError("Should implement generate_positions()!")

    @abstractmethod
    def backtest_portfolio(self):
        """
        Fornisce la logica per generare gli ordini di trading
        e la successiva curva del patrimonio netto (ovvero la
        crescita del patrimonio netto totale), come somma
        di partecipazioni e contanti, e il periodo delle barre
        associato a questa curva in base al DataFrame delle "posizioni".

        Produce un oggetto portfolio che può essere esaminato da
        altre classi / funzioni.
        """
        raise NotImplementedError("Should implement backtest_portfolio()!")


class Strategy(object):
    """
    Strategy è una classe base astratta che fornisce un'interfaccia per
    tutte le strategie di trading successive (ereditate).

    L'obiettivo di un oggetto Strategy (derivato) è produrre un elenco di segnali,
    che ha la forma di un DataFrame pandas indicizzato di serie temporale.

    In questo caso è gestito solo un singolo simbolo / strumento.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError("Should implement generate_signals()!")

    @abstractmethod
    def computed_data(self):
        raise NotImplementedError("Should implement generate_signals()!")

class StrategyTest:
    TAKE_PROFIT = 0
    STOP_LOSS = 0
    RATIO = 0

    taapi = None
    candle_value = None
    value = None
    type = None
    time = None
    ema1 = None
    ema2 = None
    ema3 = None
    ema4 = None

    def settypestrategy(self, type):
        self.type = type

    def setema(self, ema1=None, ema2=None, ema3=None, ema4=None):
        self.ema1 = ema1
        self.ema2 = ema2
        self.ema3 = ema3
        self.ema4 = ema4

    def setvaluecandle(self, candle_value):
        self.candle_value = candle_value

    def settime(self, time):
        self.time = time

    def setratio(self, ratio):
        self.RATIO = ratio

    def settakeprofit(self, takeprofit):
        self.TAKE_PROFIT = takeprofit

    def setstoploss(self, stoploss):
        self.STOP_LOSS = stoploss

    def gettypestrategy(self):
        return self.type

    def check_entry(self):

        candle_close = self.getvaluecandle()

        if self.gettypestrategy() == 'LONG':
            ratio_value = self.ema1 / self.ema2
            if 1 < ratio_value < self.getratio():
                if candle_close > self.ema3:
                    return candle_close

        if self.gettypestrategy() == 'SHORT':
            ratio_value = self.ema2 / self.ema1
            if 1 < ratio_value < self.getratio():
                if candle_close < self.ema3:
                    return candle_close

        return None

    def getratio(self):
        return self.RATIO

    def getvaluecandle(self):
        return self.candle_value

    def stop_loss(self, entry_candle_close_value, candle_close_iterate):

        if self.gettypestrategy() == 'LONG':
            if entry_candle_close_value < candle_close_iterate * self.STOP_LOSS:
                return True

        if self.gettypestrategy() == 'SHORT':
            if entry_candle_close_value < candle_close_iterate * self.STOP_LOSS:
                return True

        return False

    def take_profit(self, entry_candle_close_value, candle_close_iterate):

        if self.gettypestrategy() == 'LONG':
            if entry_candle_close_value > candle_close_iterate * self.TAKE_PROFIT:
                return True

        if self.gettypestrategy() == 'SHORT':
            if entry_candle_close_value < candle_close_iterate * self.TAKE_PROFIT:
                return True

        return False
