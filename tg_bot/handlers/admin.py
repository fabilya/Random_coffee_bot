from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from admin_panel.telegram.models import TgUser
from tg_bot.config import HOST_IP
from tg_bot.db import db_commands as db
from tg_bot.keyboards.callback_data import BlockUserCallback
from tg_bot.keyboards.inline import kb_block_unblock_user, kb_cancel
from tg_bot.middlewares.admin import AdminMiddleware
from tg_bot.misc.utils import delete_message
from tg_bot.states.all_states import Admin

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())
admin_router.callback_query.middleware(AdminMiddleware())

ADMIN_WELCOME_TEXT = (
    'Доступ к административным функциям предоставляется через '
    f'<a href="http://{HOST_IP}">сайт</a>.\n'
    'Для блокировки пользователя <b>через бот</b>, введите его почту:'
)

USER_NOT_EXIST = (
    'Такого пользователя не существует!\n'
    'Попробуйте ещё раз.'
)

ABOUT_USER = (
    '💼<b>ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:</b>💼\n'
    '__________________________________\n'
    '🔉<b>имя и фамилия:</b> {tg_model.enter_full_name}\n'
    '🔉<b>никнейм:</b> {tg_model.username}\n'
    '🔉<b>полное имя в тг:</b> {tg_model.full_name}\n'
)


@admin_router.message(Command('admin'))
async def admin_message(message: Message, state: FSMContext):
    """Предложение ввести почту."""
    msg = await message.answer(text=ADMIN_WELCOME_TEXT)
    await state.set_state(Admin.get_email)
    await delete_message(msg)


@admin_router.message(Admin.get_email)
async def get_name(message: Message):
    """Поиск пользователя в БД по введённой электронной почте."""
    tg_model: TgUser = await db.search_tg_user(message.text.lower())

    if tg_model:
        msg = await message.answer_photo(
            photo=FSInputFile(tg_model.picture.path.replace('media', 'media/TgUsers')),
            caption=ABOUT_USER.format(tg_model=tg_model),
            reply_markup=kb_block_unblock_user(tg_user=tg_model))
        await delete_message(msg)
    else:
        await message.answer(text=USER_NOT_EXIST,
                             reply_markup=kb_cancel(),
                             )


@admin_router.callback_query(Admin.get_email, F.data == 'cancel')
async def stop(callback: CallbackQuery, state: FSMContext):
    """Отмена."""
    await callback.message.answer("Вы отменили текущее действие")
    await callback.message.delete()
    await state.clear()


@admin_router.callback_query(BlockUserCallback.filter())
async def unblock(callback: CallbackQuery, callback_data: BlockUserCallback):
    """Разблокировать/заблокировать пользователя."""
    await callback.message.delete()
    user_id = callback_data.user_id
    tg_model = await db.get_tg_user(user_id)
    tg_model.is_unblocked = not callback_data.block
    await db.save_model(tg_model)

    msg = 'разблокирован' if tg_model.is_unblocked else 'заблокирован'

    msg = await callback.message.answer(
        f'Пользователь {tg_model.enter_full_name} {msg}'
    )
    await delete_message(msg)
