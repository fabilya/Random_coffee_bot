from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from admin_panel.telegram.models import TgUser
from tg_bot.handlers.main_menu import main_menu
from tg_bot.handlers.registration import start_registration
from tg_bot.middlewares.blocking import BlockingMiddleware
from tg_bot.db.db_commands import save_model

default_router = Router()
default_router.message.middleware(BlockingMiddleware())
default_router.callback_query.middleware(BlockingMiddleware())


@default_router.message(Command('start'))
async def command_start(message: Message, state: FSMContext, tg_user: TgUser):
    """Ввод команды /start"""
    if tg_user:
        if tg_user.bot_unblocked is False:
            tg_user.bot_unblocked = True
            await save_model(tg_user)
        await main_menu(message)
    else:
        await start_registration(message, state)
