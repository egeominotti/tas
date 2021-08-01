from django.core.management import BaseCommand
import logging
from strategy.models import LogicEntry
from html_sanitizer import Sanitizer

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):
        sanitizer = Sanitizer()
        for k in LogicEntry.objects.all():
            if len(k.content.html) > 0:
                sanatizer_func = sanitizer.sanitize(k.content.html)
                print(type(sanatizer_func))
                print(eval(sanatizer_func))
