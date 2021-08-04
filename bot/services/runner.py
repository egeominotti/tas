from bot.model.bot import TradingBot
from bot.models import Bot, BotLogger


def get_runnerbot_hook(task) -> None:
    """

    :param task:
    :return:None
    """
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


def runnerbot(instance, user, symbol_taapi, symbol_exchange, bot_object, logger_object):
    """
    :param symbol_taapi:
    :param symbol_exchange:
    :param instance: Oggetto che contiene l'istanza del bot con i dati
    :param bot_object: Oggetto di tipo Bot
    :param logger_object: Oggetto di tipo BotLogger
    :return: Ritorna True se il bot ha trovato un takeprofit o stoploss False se si è verificata una eccezzione
    """

    bot = TradingBot(
        current_bot=instance,
        user=user,
        symbol=symbol_taapi,
        symbol_exchange=symbol_exchange,
        time_frame=instance.strategy.time_frame.time_frame,
        func_entry=instance.strategy.logic_entry,
        func_exit=instance.strategy.logic_exit,
        logger=logger_object,
        bot_object=bot_object
    )

    if bot.run():
        item = {
            'id': instance.id,
            'time_frame': instance.strategy.time_frame.time_frame
        }

        return item

    return False
