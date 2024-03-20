from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from config import settings

NULLABLE = {
    'null': True,
    'blank': True,
}


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=100, verbose_name='место')
    date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    action = models.CharField(max_length=100, verbose_name='действие')
    is_pleasurable = models.BooleanField(default=False, verbose_name='приятная привычка')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    frequency = models.CharField(
        max_length=50,
        choices=[('day', 'раз в день'), ('week', 'раз в неделю')],
        default='day',
        verbose_name='периодичность'
    )
    reward = models.CharField(max_length=100, verbose_name='вознаграждение', **NULLABLE)
    time_required = models.DurationField(default=60, verbose_name='время выполнения')
    is_public = models.BooleanField(default=False, verbose_name='публичная привычка')

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя указывать одновременно вознаграждение и связанную привычку.")

        if self.time_required.total_seconds() > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")

        if self.related_habit and not self.related_habit.is_pleasurable:
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")

        if self.is_pleasurable and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        if self.frequency == 'week' and self.time_required.days > 7:
            raise ValidationError("Частота выполнения привычки должна быть не больше недели.")

        if self.frequency == 'day' and self.time_required.days > 1:
            raise ValidationError("Частота выполнения привычки должна быть не больше дня.")

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('date',)
