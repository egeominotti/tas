from threading import Thread

import requests
import sys


class Telegram:

    def __init__(self):
        self.bot_token = '1889367095:AAGS13rjA6xWAGvcUTOy1W1vUZvPnNxcDaw'
        self.bot_chat_id = '-558016221'

    # async send
    def async_send(self, text):
        try:

            send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chat_id + '&parse_mode=Markdown&text=' + text
            response = requests.get(send_text)
            return response.json()

        except Exception as e:
            exception = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
            print(exception)

        sys.exit()

    def send(self, text):

        thread = Thread(target=self.async_send, args=(text,))
        thread.daemon = True
        thread.start()
