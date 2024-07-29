import requests 

from datetime import datetime, timedelta
import json

### Custom functions
import sys




class TelegramManager:
    
    def __init__(self) -> None:
        self.config = self._read_config()


    def _read_config(self, file_path="/home/lucas/.creds/telegram_bot/bot_config.json"):
        with open(file_path, "r") as file:
            config = json.load(file)
        return config

    def bot_send_text(self, bot_message):
        # Leo la configuración del json 
        ()
        bot_token = self.config.get("token", 0)
        bot_chatID = self.config.get("chat_id", 0)


        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        return response


    # test_bot = bot_send_text("Buenos días máquina, hoy la bolsa ha abierto en \n" + str(text))
    

    
