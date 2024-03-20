from rest_framework import serializers
from habits.models import Habit
from habits.validators import *


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        validate_habit_fields(data)
        validate_time_required(data)
        validate_related_habit(data)
        validate_pleasurable_habit(data)
        return data
