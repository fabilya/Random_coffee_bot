from aiogram import BaseMiddleware

from tg_bot.db.db_commands import get_tg_user


class AdminMiddleware(BaseMiddleware):
    """ Проверка админ-прав пользователя """
    async def __call__(self, handler, event, data):
        if event.from_user.is_bot is False:

            user = await get_tg_user(event.from_user.id)

            if user is None or not user.is_admin:
                await event.answer(
                    text='Вы не администратор.',
                    show_alert=True
                )
                return

        await handler(event, data)
