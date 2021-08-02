from bot.model.bot import TradingBot
from bot.models import Bot, BotLogger


def get_runnerbot_hook(task):
    print("HO FINITO")
    print("HO FINITO")
    print("HO FINITO")
    print("HO FINITO")
    print("HO FINITO")
    print("HO FINITO")
    print("HO FINITO")
    print(task.result)
    print(task)
    print(task)
    if isinstance(task.result, dict):
        print("Cancello il bot")
        bt = Bot.objects.get(id=task.result.get('id'))
        BotLogger.objects.filter(bot=bt).delete()
        Bot.objects.filter(id=task.result.get('id')).delete()


def runnerbot(instance, bot_object, logger_object):

    bot = TradingBot(
        current_bot=instance,
        symbol=instance.strategy.symbol_taapi.symbol,
        symbol_exchange=instance.strategy.symbol_exchange.symbol,
        time_frame=instance.strategy.time_frame.time_frame,
        func_entry=instance.strategy.logic_entry,
        func_exit=instance.strategy.logic_exit,
        logger=logger_object,
        bot_object=bot_object
    )

    if bot.run():

        item = {
            'id': instance.id,
            'symbol': instance.strategy.symbol_exchange.symbol,
            'time_frame': instance.strategy.time_frame.time_frame
        }

        return item

    return False
