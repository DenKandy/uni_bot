import logging, threading
from telegram.ext import Updater, Handler, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class TelegramBot(object):
    def __init__(self, token: str = None, command_handlers={}):
        self.token = token
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        for name, func in command_handlers.items():
            self.add_handler(CommandHandler(name, func))

        logging.info("TelegramBot token:{} successfully initialized!".format(self.token))
    
    def add_handler(self, handler: Handler) -> None:
        self.dispatcher.add_handler(handler)

    def run(self):
        logging.info("TelegramBot token:{} started!".format(self.token))
        self.updater.start_polling()
