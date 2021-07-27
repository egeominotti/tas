from services.exchangeApi import Taapi


class BOT:
    taapi = None

    def __init__(self, symbol, time_frame, ratio, STOP_LOSS, TAKE_PROFIT):
        taapi = Taapi(symbol)
        self.time_frame = time_frame
        self.ratio = ratio
        self.stop_loss = 2
        self.take_profit = 3

    def run(self, func_entry):
        pass

        rsi = self.taapi.rsi(self.time_frame)
        bbands = self.taapi.bbands(self.time_frame)

        item = {
            'rsi': rsi.get('value'),
            'middleband': bbands.get('valueMiddleBand'),
            'lowerband': bbands.get('valueLowerBand')
        }


    def stop_loss(self):
        pass

    def take_profit(self):
        pass
