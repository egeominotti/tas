import requests


class Telegram:

    def __init__(self):
        self.bot_token = '1889367095:AAGS13rjA6xWAGvcUTOy1W1vUZvPnNxcDaw'
        self.bot_chat_id = '-558016221'

    def send(self, text):
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chat_id + '&parse_mode=Markdown&text=' + text
        response = requests.get(send_text)
        print(response.json())
        return response.json()
