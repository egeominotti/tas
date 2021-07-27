from services.exchangeApi import Taapi


class BOT:

    def __bool__(self, symbol):
        self.taapi = Taapi(symbol)
        self.symbol = symbol

    def run(self):
        pass

    def check(self):
        pass
