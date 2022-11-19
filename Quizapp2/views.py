from .models import CreamCards, QuizQuestion
from .serializers import CreamCardsSerializer,QuizQuestionSerializers
from rest_framework import generics

from datetime import timedelta
from django.utils import timezone


class CreamCardsList(generics.ListCreateAPIView):
    queryset = CreamCards.objects.all().order_by('-created_at')
    serializer_class = CreamCardsSerializer

class FreshCreamCards_delta2(generics.ListAPIView):
    serializer_class = CreamCardsSerializer

    def get_queryset(self):
        some_day_last_week = timezone.now().date() - timedelta(days = 3)
        queryset = CreamCards.objects.filter(created_at__gte=some_day_last_week).order_by('-created_at') #https://stackoverflow.com/questions/11205096/how-to-retrieve-records-from-past-weeks-in-django
        return queryset


class CreamCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreamCards.objects.all()
    serializer_class = CreamCardsSerializer


class QuizQuestionsList(generics.ListCreateAPIView):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers


class QuizQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers
