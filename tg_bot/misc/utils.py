from asyncio import sleep
from typing import Optional

from aiogram import Bot
from aiogram.types import Message, BotCommand, BotCommandScopeDefault


async def get_entered_name(text: str) -> Optional[str]:
    """Принимает текст, возвращает отформатированное полное имя или None"""
    name_parts = text.strip().split(' ')

    if len(name_parts) != 2 or not all(part.isalpha() for part in name_parts):
        return None

    return ' '.join(part.capitalize() for part in name_parts)


async def delete_message(message: Message, sleep_time: int = 600) -> None:
    """Удаляет сообщение, по умолчанию через 600 секунд"""
    await sleep(sleep_time)
    try:
        await message.delete()
    except Exception:
        return


async def set_commands(bot: Bot):
    """Функция для формирования списка команд для кнопки Menu"""
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
