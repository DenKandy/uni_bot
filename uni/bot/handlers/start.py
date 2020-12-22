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
        self.users = None
    
    def is_user_registered(self):
        from bot.models import UserUniModel
        if not self.users:
            return False
        if len(self.users) == 0:
            return False

        for user in self.users:
            telegram_id = getattr(user, UserUniModel.telegram_id_str)
            if telegram_id == self.update.message.from_user.id:
                return True

    def execute(self):
        from bot.models import GeneralUniModel, UserUniModel
        if not self.object:
            self.object = GeneralUniModel.objects.all()[0] if self.is_user_registered() else GeneralUniModel.objects.all()[1]
        if not self.users:
            self.users = UserUniModel.objects.all()

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