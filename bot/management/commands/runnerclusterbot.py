from bot.model.clusterbot import ClusteringBot
from bot.models import ClusterBot, UserExchange, BotLogger
from django.core.management import BaseCommand
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'AsyncRunnerClusterBot'

    def handle(self, *args, **kwargs):
        qs = ClusterBot.objects.all()
        print(qs)
        for k in qs:
            print(k.market_spot)
            tb = ClusteringBot(
                instance=k,
                userexchange=UserExchange.objects.get(user=k.user),
                logger=BotLogger,
                bot_object=ClusterBot
            )
            tb.run()
