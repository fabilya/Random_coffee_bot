from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Mailing, TgUser, Meeting

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'enter_full_name',
        'full_name',
        'username',
        'is_active',
        'is_unblocked',
        'bot_unblocked',
        'picture',
    )

    def has_add_permission(self, request, obj=None):
        """Убирает возможность создания пользователей через админку"""
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если редактируется существующий объект
            return self.readonly_fields + (
                'id', 'full_name', 'username', 'bot_unblocked')
        return self.readonly_fields


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'date_mailing',
        'is_sent',
    )
    readonly_fields = ('is_sent',)


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'partner',
        'date',
    )

    def has_add_permission(self, request, obj=None):
        """Убирает возможность создания через админку"""
        return False

    def has_change_permission(self, request, obj=None):
        # Запрещаем редактирование объектов
        return False
