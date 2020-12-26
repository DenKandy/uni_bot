import logging

from telegram import Update, User
from telegram.ext import CallbackContext, Handler, CommandHandler, MessageHandler, ConversationHandler, Filters

from django.conf import settings
from bot.views import RegisterUser

class Commands:
    start   = 'start'
    help    = 'help'
    share   = 'share'
    cancel  = 'cancel'
    all     = 'all'

commands_help = {
    # /name             : [ short description,                                  detail description]
    Commands.start      : ['Почати спілкування з ботом',                        'Почати спілкування з ботом'],
    Commands.help       : ['Отримати більш розгорнуту довідку по командам',     'Отримати більш розгорнуту довідку по командам'],
    Commands.share      : ['Відправлення контенту по категорії',                'Відправлення контенту по категорії'],
    Commands.cancel     : ['Припинити розмову з ботом',                         'Припинити розмову з ботом'],
}

def reply_welcome(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Ласкаво просимо в чат-бот Університету!\n'
        'Вас вітає Ваш особистий віртуальний помічник.\n')

def reply_registration_required(update: Update, context: CallbackContext, user: User) -> None:
    update.message.reply_text(
        'Ви не зареєстровані перейдіть будь ласка за посиланням {} щоб заереструватіся в системі чат-бот Університету'.format(
        '{}{}{}'.format(settings.CURRENT_HOST, RegisterUser.URL, user.id)))

def is_user_registered(user: User) -> bool:
    from bot.models import UserUniModel
    db_users = UserUniModel.objects.all()
    if db_users:
        for db_user in db_users:
            telegram_id = getattr(db_user, UserUniModel.telegram_id_str)
            if int(telegram_id) == user.id:
                return True      
    return False

def common_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Вибачте бот не має можливості обробити запит, зверніться до довідки з помощю /{}\n'.format(Commands.help))

def get_message_handler() -> MessageHandler:
    return MessageHandler(Filters.all, common_handler)