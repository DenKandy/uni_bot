"""
WSGI config for uni project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uni.settings')

application = get_wsgi_application()

from bot.telegrambot import TelegramBot
from django.conf import settings
from bot.mapping import command_handlers, message_handlers, conversation_handlers

if settings.RUN_UNIBOT:
    uni_bot = TelegramBot(settings.BOT_TOKEN, command_handlers=command_handlers, message_handlers=message_handlers, conversation_handlers=conversation_handlers)
    uni_bot.run()