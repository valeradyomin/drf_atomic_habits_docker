from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.exceptions import ValidationError
from habits.models import Habit
from users.models import User
from datetime import timedelta
from habits.validators import (
    validate_habit_fields,
    validate_time_required,
    validate_pleasurable_habit,
)


class HabitsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test1@test.sky.pro',
            password='12345',
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        response = self.client.post('/habits/create/', {
            'user': self.user.id,
            'place': 'Дом',
            'date': '2025-01-01T00:00:00+03:00',
            'action': 'Медитация',
            'is_pleasurable': False,
            'related_habit': '',
            'frequency': 'day',
            'reward': '',
            'time_required': '00:01:00',
            'is_public': False
        })
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().user, self.user)
        self.assertEqual(Habit.objects.get().place, 'Дом')
        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'user': self.user.id,
                             'place': 'Дом',
                             'date': '2025-01-01T00:00:00+03:00',
                             'action': 'Медитация',
                             'is_pleasurable': False,
                             'related_habit': None,
                             'frequency': 'day',
                             'reward': '',
                             'time_required': '00:01:00',
                             'is_public': False
                         })

    def test_habit_detail(self):
        data = {
            'user': self.user.id,
            'place': 'Дом',
            'date': '2025-01-01T00:00:00+03:00',
            'action': 'Медитация',
            'is_pleasurable': False,
            'related_habit': '',
            'frequency': 'day',
            'reward': '',
            'time_required': '00:01:00',
            'is_public': False
        }
        response = self.client.post('/habits/create/', data)
        print(response.json())

        response = self.client.get('/habits/detail/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'user': self.user.id,
                             'place': 'Дом',
                             'date': '2025-01-01T00:00:00+03:00',
                             'action': 'Медитация',
                             'is_pleasurable': False,
                             'related_habit': None,
                             'frequency': 'day',
                             'reward': '',
                             'time_required': '00:01:00',
                             'is_public': False
                         })

    def test_habit_update(self):
        data = {
            'user': self.user.id,
            'place': 'Дом',
            'date': '2025-01-01T00:00:00+03:00',
            'action': 'Медитация',
            'is_pleasurable': False,
            'related_habit': '',
            'frequency': 'day',
            'reward': '',
            'time_required': '00:01:00',
            'is_public': False
        }
        response = self.client.post('/habits/create/', data)
        print(response.json())

        data_update = {
            'user': self.user.id,
            'place': 'Дача',
            'date': '2025-01-01T00:00:00+03:00',
            'action': 'Медитация',
            'is_pleasurable': True,
            'related_habit': '',
            'frequency': 'week',
            'reward': '',
            'time_required': '00:02:00',
            'is_public': True
        }
        response = self.client.put('/habits/update/1/', data_update)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        data = {
            'user': self.user.id,
            'place': 'Дом',
            'date': '2025-01-01T00:00:00+03:00',
            'action': 'Медитация',
            'is_pleasurable': False,
            'related_habit': '',
            'frequency': 'day',
            'reward': '',
            'time_required': '00:01:00',
            'is_public': False
        }
        response = self.client.post('/habits/create/', data)
        print(response.json())

        response = self.client.delete('/habits/delete/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_habit_user_list(self):
        data = {
            'user': self.user.id,
            'place': 'Дом',
            'date': '2025-01-01T00:00:00+03:00',
            'action': 'Медитация',
            'is_pleasurable': False,
            'related_habit': '',
            'frequency': 'day',
            'reward': '',
            'time_required': '00:01:00',
            'is_public': False
        }
        response = self.client.post('/habits/create/', data)
        print(response.json())

        response = self.client.get('/habits/user_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_public_list(self):
        Habit.objects.create(
            user=self.user,
            place='Дом',
            date='2025-01-01T00:00:00+03:00',
            action='Медитация',
            is_pleasurable=False,
            related_habit=None,
            frequency='day',
            reward='',
            time_required='00:01:00',
            is_public=True
        )
        response = self.client.get('/habits/public_list/')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {
                    'id': 1,
                    'user': self.user.id,
                    'place': 'Дом',
                    'date': '2025-01-01T00:00:00+03:00',
                    'action': 'Медитация',
                    'is_pleasurable': False,
                    'related_habit': None,
                    'frequency': 'day',
                    'reward': '',
                    'time_required': '00:01:00',
                    'is_public': True
                }
            ]
            }
        )


class HabitValidatorsAPITestCase(APITestCase):
    def test_validate_habit_fields(self):
        value = {'reward': 'some_reward', 'related_habit': 'some_related_habit'}
        with self.assertRaises(ValidationError) as cm:
            validate_habit_fields(value)
        self.assertEqual(str(cm.exception), "['Нельзя указывать одновременно вознаграждение и связанную привычку.']")

    def test_validate_time_required(self):
        value = {'time_required': timedelta(seconds=121)}
        with self.assertRaises(ValidationError) as cm:
            validate_time_required(value)
        self.assertEqual(str(cm.exception), "['Время выполнения должно быть не больше 120 секунд.']")

    def test_validate_pleasurable_habit(self):
        value = {'is_pleasurable': True, 'reward': 'some_reward'}
        with self.assertRaises(ValidationError) as cm:
            validate_pleasurable_habit(value)
        self.assertEqual(str(cm.exception), "['У приятной привычки не может быть вознаграждения или связанной "
                                            "привычки.']")
