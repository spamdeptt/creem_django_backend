from .models import CreamCards, QuizQuestion, QuizQuestionCollection
from .serializers import CreamCardsSerializer,QuizQuestionSerializers, QuizQuestionCollectionSerializers
from rest_framework import generics
from rest_framework.response import Response

from datetime import timedelta
from django.utils import timezone
from django.db.models import F


class QuizQuestionsCorrect(generics.RetrieveUpdateDestroyAPIView):   #https://stackoverflow.com/questions/51736015/increment-visits-counter-from-django-rest
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        QuizQuestion.objects.filter(pk=instance.id).update(correctCount=F('correctCount') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class QuizQuestionsIncorrect(generics.RetrieveUpdateDestroyAPIView):  #https://stackoverflow.com/questions/51736015/increment-visits-counter-from-django-rest
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        QuizQuestion.objects.filter(pk=instance.id).update(inCorrectCount=F('inCorrectCount') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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


class QuizQuestionCollectionList(generics.ListCreateAPIView):
    queryset = QuizQuestionCollection.objects.all()
    serializer_class = QuizQuestionCollectionSerializers


class QuizQuestionCollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizQuestionCollection.objects.all()
    serializer_class = QuizQuestionCollectionSerializers
    