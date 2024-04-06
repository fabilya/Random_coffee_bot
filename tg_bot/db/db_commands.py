from datetime import date, timedelta

from aiogram.types.user import User
from asgiref.sync import sync_to_async
from django.utils import timezone

from admin_panel.telegram.models import Mailing, Meeting, TgUser


@sync_to_async
def create_tg_user(user: User, email: str, enter_full_name: str, picture: str):
    """Создаёт и возвращает экземпляр пользователя TgUser"""
    tg_user = TgUser.objects.create(
        id=user.id,
        email=email,
        enter_full_name=enter_full_name,
        username=user.username,
        full_name=user.full_name,
        picture=picture
    )
    return tg_user


@sync_to_async
def get_tg_user(user_id):
    """Возвращает экземпляр требуемого пользователя по id"""
    return TgUser.objects.filter(id=user_id).first()


@sync_to_async
def search_tg_user(email: str):
    """Возвращает экземпляр требуемого пользователя по email"""
    return TgUser.objects.filter(email=email).first()


@sync_to_async
def save_model(model):
    """Сохранение изменений в модели"""
    model.save()


@sync_to_async
def create_meeting(user: TgUser, partner: TgUser):
    """Создаёт и возвращает экземпляр встречи"""
    return Meeting.objects.create(user=user, partner=partner)


@sync_to_async
def get_active_users() -> set[TgUser]:
    """Возвращает множество активных пользователей"""
    return set(TgUser.objects.filter(
        is_active=True,
        is_unblocked=True,
        bot_unblocked=True,
    ))


@sync_to_async
def get_unblocked_users():
    """Возвращает всех незаблокированных пользователей"""
    return TgUser.objects.filter(
        bot_unblocked=True,
        is_unblocked=True,
    )


@sync_to_async
def get_partners_ids(user: TgUser, old: bool = False) -> set[int]:
    """
    Асинхронно извлекает и возвращает множество ID партнёров, с которыми у
    указанного пользователя была встреча. Позволяет также получить тех
    партнёров, с кем встречи были более полугода назад.

    Args:
        user: Пользователь, для которого необходимо получить ID партнёров.
        old: Если True, возвращает ID партнёров, с которыми последняя встреча
             была более полугода назад. По умолчанию False.

    Returns:
        set[int]: Множество ID партнёров в соответствии с выбранным условием.
    """
    if old:
        half_year_ago = date.today() - timedelta(days=180)
        query = user.user_meetings.filter(date__lt=half_year_ago)
    else:
        query = user.user_meetings
    return set(query.values_list('partner', flat=True))


@sync_to_async
def get_unsent_mailings():
    """Возвращает все неразосланные рассылки, чье время отправки наступило"""
    return Mailing.objects.filter(
        date_mailing__lte=timezone.now(),
        is_sent=False,
    )
