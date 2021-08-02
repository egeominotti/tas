from time import sleep
import datetime
from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from exchange.model.binance import BinanceHelper


class DispatcherBot:
    """
    Deve pilotare i trading bot in base al mercato
    """
    pass


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
            # binance,
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
        self.logger_id = None

        # self.binance = None
        # if self.current_bot.live:
        #     self.binance = BinanceHelper(
        #         api_key=binance.api_key,
        #         api_secret=binance.api_secret,
        #         symbol=symbol_exchange,
        #         quantity=quantity_investment,
        #         leverage=leverage
        #     )

    # def stop(self):
    #     execution = self.bot_object.objects.get(id=self.current_bot.id).execution
    #     if execution is False:
    #         now = datetime.datetime.now()
    #         self.bot_object.objects.filter(id=self.current_bot.id).update(execution=False)
    #         start = "BOT stopped:" + "symbol: " + str(self.symbol) + " time frame: " + str(
    #             self.time_frame) + " stopped at: " + str(now)
    #         self.telegram.send(start)
    #         return True

    def start(self):

        self.logger_id = self.logger.objects.create(bot=self.current_bot)

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        print(self.current_bot.name)
        print(self.symbol)
        print(self.time_frame)

        start = "Started: " + str(self.current_bot.name) + \
                "\n" + "Symbol: " + str(self.symbol) + \
                "\nTime frame: " + str(self.time_frame) + \
                "\nStarted at: " + str(now) + \
                "\nLet's go to the moon 🚀️"
        self.telegram.send(start)

    def run(self, sleep_time_position=0, sleep_time_profit_or_loss=0):

        open_position_value = 0
        position = False

        self.start()

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

                    func_entry_value = self.func_entry(item=item, bot=True)
                    if isinstance(func_entry_value, Exception):
                        error = "ERROR" + str(func_entry_value)
                        self.telegram.send(error)

                    if isinstance(func_entry_value, float):

                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        entry_text = "Bot: " + str(self.current_bot.name) + "\n" \
                                     "\n" + "Symbol: " + str(self.symbol) + \
                                     "\nTime frame: " + str(self.time_frame) + \
                                     "\nEntry Candle value: " + str(func_entry_value) + \
                                     "\nEntry Candel date: " + str(now)
                        self.telegram.send(entry_text)

                        now = datetime.datetime.now()
                        self.logger.objects.filter(id=self.logger_id.id).update(
                            entry_candle=func_entry_value,
                            entry_candle_date=now,
                        )

                        # self.logger.objects.create(
                        #     entry_candle=func_entry_value,
                        #     entry_candle_date=now,
                        #     bot=self.current_bot
                        # )

                        # if self.current_bot.live:
                        #     self.binance.buy()

                        open_position_value = func_entry_value
                        position = True

                sleep(sleep_time_position)

                """
                Se viene aperta una posizione allora verifica le condizioni stoploss e takeprofit
                """
                if position is True:
                    print("Provo a cercare una take profit o stop loss")
                    value = self.func_stop_loss(item=item, bot=True)

                    if isinstance(value, Exception):
                        error = "ERROR" + str(value)
                        self.telegram.send(error)
                        break

                    if isinstance(value, float):

                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        stop_loss = "Bot: " + str(self.current_bot.name) + "\n" \
                                     "\n" + "Symbol: " + str(self.symbol) + \
                                     "\nTime frame: " + str(self.time_frame) + \
                                     "\nStop loss candle value: " + str(value) + \
                                     "\nStop loss candle date: " + str(now)
                        self.telegram.send(stop_loss)

                        # now = datetime.datetime.now()
                        #  self.logger.objects.create(
                        #      candle_take_profit=value,
                        #      candle_take_profit_date=now,
                        #      stop_loss=True,
                        #    bot=self.current_bot
                        # )
                        now = datetime.datetime.now()
                        self.logger.objects.filter(id=self.logger_id.id).update(
                            candle_take_profit=value,
                            candle_take_profit_date=now,
                            stop_loss=True,
                        )
                        #
                        # if self.current_bot.live:
                        #     self.binance.sell()

                        break

                    value = self.func_take_profit(item=item, bot=True)
                    if isinstance(value, Exception):
                        error = "ERROR" + str(value)
                        self.telegram.send(error)
                        break

                    if isinstance(value, float):

                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        take_profit = "Bot: " + str(self.current_bot.name) + "\n" \
                                     "\n" + "Symbol: " + str(self.symbol) + \
                                     "\nTime frame: " + str(self.time_frame) + \
                                     "\nTake Profit candle value: " + str(value) + \
                                     "\nTake profit candle date: " + str(now)
                        self.telegram.send(take_profit)

                        now = datetime.datetime.now()
                        self.logger.objects.filter(id=self.logger_id.id).update(
                            candle_stop_loss=value,
                            candle_stop_loss_date=now,
                            take_profit=True,
                        )

                        # if self.current_bot.live:
                        #     self.binance.sell()

                        break



            except Exception as e:
                start = "Errore imprevisto nel bot: " + str(e)
                self.telegram.send(start)
                break
