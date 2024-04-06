from aiogram import BaseMiddleware

from tg_bot.db.db_commands import get_tg_user


class BlockingMiddleware(BaseMiddleware):
    """Middleware для проверки заблокированных пользователей"""
    async def __call__(self, handler, event, data):
        if event.from_user.is_bot is False:

            user = await get_tg_user(event.from_user.id)

            if user is not None and not user.is_unblocked:
                await event.answer(
                        text='Вы заблокированы.',
                        show_alert=True
                    )
                return
            data['tg_user'] = user
        await handler(event, data)
