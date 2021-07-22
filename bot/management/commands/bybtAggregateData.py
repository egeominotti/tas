from django.core.management import BaseCommand
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        pass
