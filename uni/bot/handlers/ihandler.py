from telegram import Update
from telegram.ext import CallbackContext
import logging

class HandlerException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class IHandler:
    def __init__(self, update: Update, context: CallbackContext):
        self.update = update
        self.context = context
        self.object = None
    
    def handle_safe(self, handle):
        try:
            handle(self)
        except (HandlerException, Exception) as e:
            logging.exception(e)
            self.update.message.reply_text("Unexpected error, please contact @who_are_you_7")
