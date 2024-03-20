from pytz import timezone
import pytz
from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from config import settings
from habits.models import Habit
from habits.services import TelegramBot

tg_bot = TelegramBot()


@shared_task
def send_telegram_notification():
    time_zone = settings.TIME_ZONE
    current_time = datetime.now(pytz.timezone(time_zone))
    usefull_habits_list = Habit.objects.filter(is_pleasurable=False)

    for habit in usefull_habits_list:
        local_date = habit.date.astimezone(timezone.get_current_timezone())
        formatted_date = local_date.strftime('%Y-%m-%d %H:%M')
        message_main = (f'{habit.user.first_name} вам необходимо выполнить привычку - {habit.action} в {formatted_date}'
                        f'\nЕё нужно выполнить за {habit.time_required} в {habit.place}.\n')

        if habit.frequency == 'day' and habit.date <= current_time:
            habit.date = datetime.now(pytz.timezone(time_zone)) + timedelta(days=1)
            formatted_next_date = habit.date.strftime('%Y-%m-%d %H:%M')

            if habit.reward or habit.related_habit:
                text_reward = habit.reward if habit.reward else habit.related_habit
                message_extended = (f'\nПосле вы получите вознаграждение - {text_reward}.\n'
                                    f'\nДалее ваша привычка должна быть выполнена завтра до {formatted_next_date}.')
            else:
                message_extended = f'\nДалее ваша привычка должна быть выполнена завтра до {formatted_next_date}.'

            message = message_main + message_extended
            tg_bot.send_message(chat_id=habit.user.telegram, text=message)
            habit.save()

        elif habit.frequency == 'week' and habit.date <= current_time:
            habit.date = datetime.now(pytz.timezone(time_zone)) + timedelta(days=7)
            formatted_next_date = habit.date.strftime('%Y-%m-%d %H:%M')

            if habit.reward or habit.related_habit:
                text_reward = habit.reward if habit.reward else habit.related_habit
                message_extended = (f'\nПосле вы получите вознаграждение - {text_reward}.\n'
                                    f'\nДалее ваша привычка '
                                    f'должна быть выполнена в течении недели до {formatted_next_date}.')
            else:
                message_extended = (f'\nДалее ваша привычка '
                                    f'должна быть выполнена в течении недели до {formatted_next_date}.')

            message = message_main + message_extended
            tg_bot.send_message(chat_id=habit.user.telegram, text=message)
            habit.save()
