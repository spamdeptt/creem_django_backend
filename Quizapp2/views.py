from .models import Creamcard, QuizQuestion, QuizQuestionCollection, Student
from .serializers import CreamCardsSerializer,QuizQuestionSerializers, QuizQuestionCollectionSerializers, StudentSerializer, StudentSavedSerializer
from .permissions import IsAdminOrReadOnly

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django_auto_prefetching import AutoPrefetchViewSetMixin

from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from django.db.models.aggregates import Count

class CreamCardsViewSet(ModelViewSet):
    serializer_class = CreamCardsSerializer
    permission_classes = [IsAdminOrReadOnly]
    #can filter using delta from query (Mosh 3.10-filtering)
    def get_queryset(self): 
        queryset = Creamcard.objects.select_related('subject').select_related('author').all().order_by('-created_at')
        delta = self.request.query_params.get('delta')
        if delta is not None:
            some_day_last_week = timezone.now().date() - timedelta(days = int(delta))
            queryset = Creamcard.objects.select_related('subject').select_related('author').filter(created_at__gte=some_day_last_week).order_by('-created_at') #https://stackoverflow.com/questions/11205096/how-to-retrieve-records-from-past-weeks-in-django
        return queryset

class QuizQuestionsViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializers
    permission_classes = [IsAdminOrReadOnly]

class QuizQuestionsCollectionViewSet(ModelViewSet):
    queryset = QuizQuestionCollection.objects.prefetch_related('collection_questions').all()
    serializer_class = QuizQuestionCollectionSerializers
    permission_classes = [IsAdminOrReadOnly]


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes=[IsAdminUser]


    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (student) = Student.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data) 
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def saved(self, request):
        (student) = Student.objects.prefetch_related('saved__subject').get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = StudentSavedSerializer(student)
            return Response(serializer.data) 
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)





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