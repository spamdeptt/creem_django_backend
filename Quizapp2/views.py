from .models import CreamCards, QuizQuestion, QuizQuestionCollection
from .serializers import CreamCardsSerializer,QuizQuestionSerializers, QuizQuestionCollectionSerializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from datetime import timedelta
from django.utils import timezone
from django.db.models import F


class CreamCardsViewSet(ModelViewSet):
    serializer_class = CreamCardsSerializer

    #can filter using delta from query (Mosh 3.10-filtering)
    def get_queryset(self): 
        queryset = CreamCards.objects.select_related('subject').select_related('author').all().order_by('-created_at')
        delta = self.request.query_params.get('delta')
        if delta is not None:
            some_day_last_week = timezone.now().date() - timedelta(days = int(delta))
            queryset = CreamCards.objects.select_related('subject').select_related('author').filter(created_at__gte=some_day_last_week).order_by('-created_at') #https://stackoverflow.com/questions/11205096/how-to-retrieve-records-from-past-weeks-in-django
        return queryset


class QuizQuestionsViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers

class QuizQuestionsCollectionViewSet(ModelViewSet):
    queryset = QuizQuestionCollection.objects.prefetch_related('collection_questions').all()
    serializer_class = QuizQuestionCollectionSerializers







#-------- 
class QuizQuestionCorrectViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        QuizQuestion.objects.filter(pk=instance.id).update(correctCount=F('correctCount') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class QuizQuestionIncorrectViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        QuizQuestion.objects.filter(pk=instance.id).update(inCorrectCount=F('inCorrectCount') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)