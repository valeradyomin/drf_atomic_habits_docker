from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.permissions import IsOwner
from habits.serializers import HabitsSerializer


class CreateHabitsAPIView(generics.CreateAPIView):
    serializer_class = HabitsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailHabitsAPIView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsOwner]


class UpdateHabitsAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsOwner]


class DeleteHabitsAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsOwner]


class UserListHabitsAPIView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicListHabitsAPIView(generics.ListAPIView):
    serializer_class = HabitsSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
