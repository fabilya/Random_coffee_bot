from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile


from admin_panel.telegram.models import TgUser
from tg_bot.db.db_commands import get_tg_user, save_model
from tg_bot.keyboards.callback_data import ParticipationCallback
from tg_bot.keyboards.inline import kb_yes_or_no
from tg_bot.middlewares.blocking import BlockingMiddleware
from tg_bot.keyboards.reply import kb_main_menu
from tg_bot.misc.utils import delete_message


main_menu_router = Router()
main_menu_router.message.middleware(BlockingMiddleware())
main_menu_router.callback_query.middleware(BlockingMiddleware())

MSG_SUSPEND = (
    'Если вы передумали принимать участие в какую-либо неделю или уходите в '
    'отпуск, то можно приостановить участие в проекте.\n'
    '\n'
    'Хотите приостановить участие?'
)

APPLY_SUSPEND = 'Вы успешно приостановили участие'
RESUME_PARTICIPATION = 'Вы успешно возобновили участие'

MSG_REVIEW = (
    '<b>Милена Мелкова, Cпециалист по продукту.</b>\n'
    '«Кофе вслепую» - отличная возможность познакомиться с коллегами '
    'из других отделов, в том числе с менеждерами и Директорами, которые '
    'тоже участвуют в проекте.\n'
    '\n'
    '<b>Анастасия Родкина, Младший менеджер по работе с ключевыми '
    'клиентами.</b>\n'
    'Крутая возможность пообщаться, лучше узнать новых сотрудников, '
    'наладить неформальный контакт в условиях удаленной работы… '
    'Поделиться своим опытом и получить заряд позитива! В крупных '
    'компаниях как наша - это необходимо! Спасибо за классный проект!\n'
    '\n'
    '<b>Анна Борисевич, Старший специалист по цифровому контенту.</b>\n'
    'Мне безумно нравится эта инициатива! Уникальная возможность '
    'быстро познакомиться с коллегами, узнать что-то новое и зарядиться '
    'позитивной энергией на весь день 🤩Всем новичкам и бывалым искренне '
    'советую попробовать поучаствовать и получить приятные впечатления 🥰'
)

GREETING_TEXT = (
    'Что умеет этот бот?\n'
    '☕️Мы продолжаем нашу прекрасную традицию знакомиться за чашечкой '
    'горячего кофе или чая.\n'
    '🗓️ С кем ты разделишь капучино - решает случай. Каждый понедельник '
    'в этом боте будет происходить рассылка с именем коллеги, '
    'с кем вам нужно организовать встречу.\n'
    '🔁Участники выбираются случайным образом, поэтому вы сможете выпить '
    'кофе с теми, с кем еще не пересекались по работе.\n'
    'Добро пожаловать🥰')

ABOUT_TEXT = '''
В нашей компании есть прекрасная традиция знакомиться за чашечкой горячего кофе в Microsoft Teams или в офисе.
Раз в неделю будет автоматически приходить имя и фамилия коллеги в этот чат-бот, вам остается договориться
о дате и времени встречи в удобном для вас формате.
«Кофе вслепую»- это всегда:
    - Прекрасная компания;
    - Приятный и неожиданный сюрприз;
    - Помощь новым коллегам в адаптации;
    - Новые знакомства.
'''  # noqa


async def main_menu(message: Message):
    """Главное меню"""
    tg_user = await get_tg_user(message.from_user.id)
    await message.answer_photo(
        photo=FSInputFile('logo.jpg'), caption=GREETING_TEXT,
        reply_markup=kb_main_menu(include_resume_button=tg_user.is_active)
    )


@main_menu_router.message(F.text == 'Приостановить участие')
async def suspend_participation(message: Message):
    """Приостановление участия."""
    msg = await message.answer(
        MSG_SUSPEND,
        reply_markup=kb_yes_or_no())
    await delete_message(msg)


@main_menu_router.message(F.text == 'Возобновить участие')
async def resume_participation(message: Message, tg_user: TgUser):
    """Возобновление участия."""
    tg_user.is_active = True
    await save_model(tg_user)
    msg = await message.answer(
        RESUME_PARTICIPATION,
        reply_markup=kb_main_menu(include_resume_button=tg_user.is_active))
    await delete_message(msg)


@main_menu_router.callback_query(ParticipationCallback.filter())
async def answer_suspend_participation(callback: CallbackQuery,
                                       callback_data: ParticipationCallback,
                                       tg_user: TgUser):
    """Приостановление участия."""
    if callback_data.is_active is True:
        await callback.message.delete()
        tg_user.is_active = not callback_data.is_active
        await save_model(tg_user)
        await callback.message.answer(
            APPLY_SUSPEND,
            reply_markup=kb_main_menu(include_resume_button=tg_user.is_active))
    else:
        await callback.message.delete()


@main_menu_router.message(F.text == 'О проекте')
async def about_project(message: Message):
    """ Раздел о проекте """
    await message.answer(ABOUT_TEXT)


@main_menu_router.message(F.text == 'Наши коллеги про проект «Кофе вслепую»')
async def reviews(message: Message):
    """Сообщение о проекте."""
    await message.answer(MSG_REVIEW)
