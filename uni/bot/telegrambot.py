import logging, threading
from telegram.ext import Updater, Handler, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class TelegramBot(threading.Thread):

    def __new__(self, token, command_handlers):
        if not hasattr(self, 'instance'):
            self.instance = super(TelegramBot, self).__new__(self)
        return self.instance

    def __init__(self, token: str = None, command_handlers={}):
        threading.Thread.__init__(self)
        self.token = token
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        for name, func in command_handlers.items():
            self.add_handler(CommandHandler(name, func))

        logging.info("TelegramBot token:{} succesfully initialized!".format(self.token))
    
    def add_handler(self, handler: Handler) -> None:
        self.dispatcher.add_handler(handler)

    def run(self):
        logging.info("TelegramBot token:{} started!".format(self.token))
        self.updater.start_polling()
        
        #//TODO Implement close event
        while True:
            pass
