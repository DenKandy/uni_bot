import logging, threading
from telegram.ext import Updater, Handler, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class TelegramBot(object):
    def __init__(self, token = None, command_handlers={}, message_handlers={}, conversation_handlers={}):
        self.token = token
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        for name, handler in command_handlers.items():
            logging.info("Add handler for command: /{}".format(name))
            self.add_handler(handler)
        
        for name, handler in conversation_handlers.items():
            logging.info("Add handler for conversation category -> {}".format(name))
            self.add_handler(handler)
        
        for name, handler in message_handlers.items():
            logging.info("Add handler for message category -> {}".format(name))
            self.add_handler(handler)

        logging.info("TelegramBot token:{} successfully initialized!".format(self.token))
    
    def add_handler(self, handler):
        self.dispatcher.add_handler(handler)

    def run(self):
        logging.info("TelegramBot token:{} started!".format(self.token))
        self.updater.start_polling()
