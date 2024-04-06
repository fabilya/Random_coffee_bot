from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_main_menu(include_resume_button=True):
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text='О проекте')
    reply_keyboard.button(text='Наши коллеги про проект «Кофе вслепую»')
    if include_resume_button:
        reply_keyboard.button(text='Приостановить участие')
    else:
        reply_keyboard.button(text='Возобновить участие')
    reply_keyboard.adjust(2, 2)
    return reply_keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите кнопку'
    )
