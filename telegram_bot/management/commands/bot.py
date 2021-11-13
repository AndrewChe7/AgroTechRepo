import logging
from typing import List
from django.core.management.base import BaseCommand, CommandError
from telegram.message import Message
from ... import models as bot_models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from AgroHackMarketplace.settings import BOT_TOKEN

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def add_messages_on_clear(context: CallbackContext, *messages: Message) -> None:
    lst = context.chat_data.setdefault("_messages_on_delete", [])
    for message in messages:
        lst.append(message)


def clear_messages(context: CallbackContext):
    lst = context.chat_data.setdefault("_messages_on_delete", [])
    for message in lst:
        res = message.delete()
    del context.chat_data["_messages_on_delete"]
    

def add_chatid(user: User, chat_id: int):
    user.telegram_info.chat_id = chat_id
    user.telegram_info.save()


def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""

    update.message.reply_text('Здравствуйте! Проверяем, привязали ли вы учетную запись к боту.\n...')
    info = bot_models.TelegramInfo.objects.filter(chat_id=update.message.from_user.id).first()
    if info is None:
        message = update.message.reply_text('''Похоже, вы не привязали свой телеграмм-аккаунт к учётной записи на нашем сайте.\nВведите логин:''')
        context.chat_data['entering_login'] = 1
        add_messages_on_clear(context, update.message, message)
    else:
        update.message.reply_text(f'Добро пожаловать, {info.user.first_name}')


def on_message(update: Update, context: CallbackContext) -> None:
    if context.chat_data.get('entering_login', 0):
        del context.chat_data['entering_login']
        context.chat_data['login'] = update.message.text
        message = update.message.reply_text('Введите пароль:')
        context.chat_data['entering_password'] = 1
        add_messages_on_clear(context, update.message, message)

    elif context.chat_data.get('entering_password', 0):
        add_messages_on_clear(context, update.message)
        del context.chat_data['entering_password']
        login = context.chat_data['login']
        del context.chat_data['login']
        password = update.message.text
        user = authenticate(username=login, password=password)
        clear_messages(context)
        if user is not None:
            add_chatid(user, update.message.chat_id)
            update.message.reply_text(f'Добро пожаловать, {user.first_name}')
        else:
            message = update.message.reply_text('Неправильный логин или пароль\nВведите логин:')
            add_messages_on_clear(context, message)
            context.chat_data['entering_login'] = 1


def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, callback=on_message))

    updater.start_polling()
    updater.idle()


class Command(BaseCommand):
    help = "Runs telegram bot"
    
    def handle(self, *args, **kwargs) -> None:
        main()
