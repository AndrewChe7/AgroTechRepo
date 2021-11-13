import logging
from typing import List
from django.core.management.base import BaseCommand, CommandError
from telegram.message import Message
from ... import models as bot_models
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, User
from AgroHackMarketplace.settings import BOT_TOKEN
from UserSystem import models as usersys_models
from pathlib import Path
from AgroHackMarketplace.settings import MEDIA_ROOT
from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
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

def get_user_from_update(update: Update) -> User:
    try:
        user = User.objects.get(telegram_info__chat_id=update.message.chat_id)
    except User.DoesNotExist:
        user = AnonymousUser()
    finally:
        return user


def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""

    update.message.reply_text('Здравствуйте! Проверяем, привязали ли вы учетную запись к боту.\n...')
    info = bot_models.TelegramInfo.objects.filter(chat_id=update.message.from_user.id).first()
    if info is None:
        message = update.message.reply_text('''Похоже, вы не привязали свой телеграмм-аккаунт к учётной записи на нашем сайте.\nВведите логин:''')
        context.chat_data['entering_login'] = 1
        add_messages_on_clear(context, update.message, message)
    else:
        keyboard = None
        update.message.reply_text(f'Добро пожаловать, {info.user.first_name}')
        if info.user.user_info.user_type in (usersys_models.UserTypes.RETAIL_PURCHASER, usersys_models.UserTypes.WHOLESALE_PURCHASER):
            keyboard = [["/requests"]]
        if keyboard is not None:
            keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text("/requests - список выставленных вами запросов на товары", reply_markup=keyboard)


def requests(update: Update, context: CallbackContext) -> None:
    user = get_user_from_update(update)
    if isinstance(user, AnonymousUser):
        update.message.reply_text("Попался, анонимус! ТЫ НЕ ПРОЙДЕШЬ НЕ ЗАРЕГИСТРИРОВАВШИСЬ!")
    elif user.user_info.user_type not in (usersys_models.UserTypes.RETAIL_PURCHASER, usersys_models.UserTypes.WHOLESALE_PURCHASER):
        update.message.reply_text("Только закупщики имеют доступ к списку заказов.")
    else:
        reqs = user.goods_requests.all()
        if reqs.count() == 0:
            update.message.reply_text("У вас ещё нет заказов.")
        else:
            for req in reqs:
                name = req.name
                description = req.description
                price = req.price
                amount = req.amount
                categories = [category.name for category in req.categories.all()]
                images = req.images.all()
                path = None
                if images.count() > 0:
                    path = images[0].image.path
                if path:
                    with open(path, mode="rb") as f:
                        message = update.message.reply_photo(f)
                    update.message.reply_text(f"<b>{name}</b>\n\nКатегории: {', '.join(categories)}\n\n{description}\n\nСтоимость максимальная за ед. товара: {price} руб.\n\nКоличество ед. товара: {amount}", reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
                else:
                    update.message.reply_text(f"<b>{name}</b>\n\n{description}", parse_mode=ParseMode.HTML)
        keyboard = [["/requests"]]
        keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text("/requests - список выставленных вами запросов на товары", reply_markup=keyboard)




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
            keyboard = [["/requests"]]
            keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text("/requests - список выставленных вами запросов на товары", reply_markup=keyboard)
        else:
            message = update.message.reply_text('Неправильный логин или пароль\nВведите логин:')
            add_messages_on_clear(context, message)
            context.chat_data['entering_login'] = 1


updater = Updater(BOT_TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("requests", requests))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, callback=on_message))


def send_notification(user: User, text: str):
    bot = updater.bot
    bot.send_message(user.telegram_info.chat_id, text)


class Command(BaseCommand):
    help = "Runs telegram bot"

    def handle(self, *args, **kwargs) -> None:
        updater.start_polling()
        updater.idle()
