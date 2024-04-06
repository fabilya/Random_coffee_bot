from aiogram.filters.callback_data import CallbackData


class BlockUserCallback(CallbackData, prefix='blocked'):
    user_id: int  # ID пользователя
    block: bool  # Блокирование пользователя


class ParticipationCallback(CallbackData, prefix='participation'):
    is_active: bool  # активация пользователя в программе
