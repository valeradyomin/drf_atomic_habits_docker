from django.contrib import admin
from habits.models import Habit


# Register your models here.
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'place',
        'date',
        'action',
        'is_pleasurable',
        'related_habit',
        'frequency',
        'reward',
        'time_required',
        'is_public'
    )
    search_fields = (
        'user',
        'place',
        'date',
        'action',
        'is_pleasurable',
        'related_habit',
        'frequency',
        'reward',
        'time_required',
        'is_public'
    )
