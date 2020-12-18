import logging

from bot.handlers.ihandler import *

class StartCommand(IHandler):
    NAME = 'start'
    @staticmethod
    def executor(update: Update, context: CallbackContext) -> None:
        command = StartCommand(update, context)
        command.handle_safe(command.execute)

    def __init__(self, update: Update, context: CallbackContext):
        self.update = update
        self.context = context
        self.object = None
    
    def execute(self, func):
        from bot.models import GeneralUniModel
        if not self.object:
            self.object = GeneralUniModel.objects.first()

        if self.object:
            value = getattr(self.object, GeneralUniModel.field_name)
            if value:
                self.update.message.reply_html(value)
            else:
                raise HandlerException(
                    "Unable to get data from '{GeneralUniModel.__name__}', field: {}. -> Check filed names".format(GeneralUniModel.field_name))
        else:
            raise HandlerException(
                    "Unable to get '{GeneralUniModel.__name__}' model. -> Check existing of table instance")