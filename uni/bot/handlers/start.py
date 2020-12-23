import logging

from bot.handlers.ihandler import *
from bot.handlers.command import commands_disc
from django.conf import settings
from bot.views import RegisterUser

from telegram import User, Bot

class StartCommand(IHandler):
    NAME = 'start'
    @staticmethod
    def executor(update: Update, context: CallbackContext) -> None:
        command = StartCommand(update, context)
        command.handle_safe(command.execute)

    def __init__(self, update: Update, context: CallbackContext)-> None:
        self.update = update
        self.context = context
        self.object = None
        self.users = None

    def __reply_for_registered_user(self) -> None:
        message = "Ласкаво просимо в чат-бот Університету!\n" + "Вас вітає Ваш особистий віртуальний помічник.\n" + "Для реалізація запитів використовуйте, будь ласка, наступні команди:\n"

        for command, desc in commands_disc.items():
            message = message + "/" + command + " " + desc + "\n"
        self.update.message.reply_text(message)
    
    def __reply_for_unregistered_user(self, user: User) -> None:
        message = "Ласкаво просимо в чат-бот Університету!\n" + "Вас вітає Ваш особистий віртуальний помічник.\n" + "Ви не зареестрованi перейдiть будьласка за посыланням щоб заереструватися в системi Uni "
        message = message + settings.CURRENT_HOST +  RegisterUser.URL + "{}".format(user.id)
        # self.update.message.reply_text(message)
        user.bot.send_message(user.id, message)

    def is_user_registered(self)-> bool:
        from bot.models import UserUniModel
        if not self.users:
            return False
        if len(self.users) == 0:
            return False

        for user in self.users:
            telegram_id = getattr(user, UserUniModel.telegram_id_str)
            if int(telegram_id) == self.update.message.from_user.id:
                return True
        return False

    def execute(self)-> None:
        from bot.models import UserUniModel
        self.users = UserUniModel.objects.all()
        if self.is_user_registered():
            self.__reply_for_registered_user()
        else:
            self.__reply_for_unregistered_user(self.update.message.from_user)