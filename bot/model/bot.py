from time import sleep
import datetime
from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from exchange.model.binance import BinanceHelper


class TradingBot:

    def __init__(
            self,
            current_bot,
            symbol,
            symbol_exchange,
            time_frame,
            ratio,
            stop_loss,
            leverage,
            quantity_investment,
            take_profit,
            func_entry,
            func_stop_loss,
            func_take_profit,
            binance,
            logger,
            bot_object
    ):
        self.current_bot = current_bot
        self.telegram = Telegram()
        self.symbol = symbol
        self.symbol_exchange = symbol_exchange
        self.taapi = Taapi(symbol)
        self.time_frame = time_frame
        self.ratio = ratio
        self.stop_loss = stop_loss
        self.leverage = leverage
        self.quantity_investment = quantity_investment
        self.take_profit = take_profit
        self.func_entry = func_entry
        self.func_stop_loss = func_stop_loss
        self.func_take_profit = func_take_profit
        self.logger = logger
        self.bot_object = bot_object

        self.binance = None
        if self.current_bot.live:
            self.binance = BinanceHelper(
                api_key=binance.api_key,
                api_secret=binance.api_secret,
                symbol=symbol_exchange,
                quantity=quantity_investment,
                leverage=leverage
            )

    def stop(self):

        # if not self.bot_object.objects.filter(id=self.current_bot.id).exists():
        #     return True

        status = self.bot_object.objects.get(id=self.current_bot.id).status
        if status == 'STOP':
            now = datetime.datetime.now()
            self.bot_object.objects.filter(id=self.current_bot.id).update(execution=False)
            start = "BOT stopped:" + "symbol: " + str(self.symbol) + " time frame: " + str(
                self.time_frame) + " stopped at: " + str(now)
            self.telegram.send(start)
            return True

    def start(self):

        self.bot_object.objects.filter(id=self.current_bot.id).update(execution=True)
        self.logger.objects.create(bot=self.current_bot)

        now = datetime.datetime.now()
        start = "BOT started:" + "symbol: " + str(self.symbol) + " time frame: " + str(
            self.time_frame) + " started at: " + str(now)
        self.telegram.send(start)

    def run(self, sleep_time_position=0, sleep_time_profit_or_loss=0):

        self.start()

        open_position_value = 0
        position = False

        while True:

            item = {
                'stop_loss': self.stop_loss,
                'take_profit': self.take_profit,
                'open_position_value': open_position_value,
                'symbol': self.symbol,
                'time_frame': self.time_frame,
                'ratio': self.ratio
            }

            try:

                """
                Finche non viene trovata una entry utile continua ad eseguire
                """
                if position is False:

                    if self.stop():
                        break
                    sleep(sleep_time_position)

                    func_entry_value = self.func_entry(item=item, bot=True)

                    if isinstance(func_entry_value, Exception):
                        error = "ERROR" + str(func_entry_value)
                        self.telegram.send(error)

                    if isinstance(func_entry_value, float):
                        now = datetime.datetime.now()
                        emtry_text = "ENTRY: " + " candela: " + str(func_entry_value) + " time: " + str(now)
                        self.telegram.send(emtry_text)

                        self.logger.objects.create(
                            entry_candle=func_entry_value,
                            entry_candle_date=now,
                            bot=self.current_bot
                        )

                        open_position_value = func_entry_value
                        position = True

                """
                Se viene aperta una posizione allora verifica le condizioni stoploss e takeprofit
                """
                if position is True:

                    if self.stop():
                        break
                    sleep(sleep_time_profit_or_loss)

                    value = self.func_stop_loss(item=item, bot=True)

                    if isinstance(value, Exception):
                        error = "ERROR" + str(value)
                        self.telegram.send(error)
                        break

                    if value is True:
                        stop_loss_text = "STOP LOSS: " + str(open_position_value * self.stop_loss)
                        self.telegram.send(stop_loss_text)

                        now = datetime.datetime.now()
                        self.logger.objects.create(
                            candle_take_profit=value,
                            candle_take_profit_date=now,
                            bot=self.current_bot
                        )

                        position = False

                    value = self.func_take_profit(item=item, bot=True)

                    if isinstance(value, Exception):
                        error = "ERROR" + str(value)
                        self.telegram.send(error)
                        break

                    if value is True:
                        take_profit_text = "TAKE_PROFIT: " + str(open_position_value * self.take_profit)
                        self.telegram.send(take_profit_text)

                        now = datetime.datetime.now()
                        self.logger.objects.create(
                            candle_stop_loss=value,
                            candle_stop_loss_date=now,
                            bot=self.current_bot
                        )

                        position = False

            except Exception as e:
                self.bot_object.objects.filter(id=self.current_bot.id).update(status='STOP')
                self.bot_object.objects.filter(id=self.current_bot.id).update(execution=False)
                start = "Errore imprevisto nel bot: " + str(e)
                self.telegram.send(start)
                break
