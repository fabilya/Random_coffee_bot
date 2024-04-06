from aiogram.utils.keyboard import InlineKeyboardBuilder

from admin_panel.telegram.models import TgUser
from tg_bot.keyboards.callback_data import (
    BlockUserCallback,
    ParticipationCallback,
)


def kb_block_unblock_user(tg_user: TgUser):
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Заблокировать' if tg_user.is_unblocked else 'Разблокировать',
        callback_data=BlockUserCallback(user_id=tg_user.id,
                                        block=tg_user.is_unblocked),
    )
    builder.button(
        text='Отмена',
        callback_data='cancel',
    )
    return builder.as_markup()


def kb_cancel():
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Отмена',
        callback_data='cancel',
    )
    return builder.as_markup()


def kb_yes_or_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Да',
        callback_data=ParticipationCallback(is_active=True),
    )
    builder.button(
        text='Нет',
        callback_data=ParticipationCallback(is_active=False),
    )
    return builder.as_markup()
