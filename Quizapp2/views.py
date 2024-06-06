from .models import Creamcard, QuizQuestion, QuizQuestionCollection, Student, Trending, FLTCollection, TrendingArchive, BlogCardButton
from .serializers import CreamCardsSerializer,QuizQuestionSerializers, QuizQuestionCollectionSerializers, StudentSerializer, StudentSavedCardsGetSerializer,StudentSavedCardsPutSerializer, StudentAccuracySerializer, TrendingTopicsSerializer, FLTCollectionSerializer, TrendingArchiveSerializer, CreamCardIDSerializer, BlogCardButtonSerializer
from .permissions import IsAdminOrReadOnly

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status

from django_auto_prefetching import AutoPrefetchViewSetMixin

from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from django.db.models.aggregates import Count
import pytz

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

class PublishedCreamCardsIDViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CreamCardIDSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Creamcard.objects.only('id').order_by('-created_at')
        delta = self.request.query_params.get('delta')
        if delta is not None:
            some_day_last_week = timezone.now().date() - timedelta(days=int(delta))
            queryset = queryset.filter(created_at__gte=some_day_last_week)
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
    def saved_cards(self, request):
        (student) = Student.objects.prefetch_related('saved_cards__subject').get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = StudentSavedCardsGetSerializer(student)
            return Response(serializer.data) 
        elif request.method == 'PUT':
            serializer = StudentSavedCardsPutSerializer(student, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def correct_incorrect_data(self, request):
        student = Student.objects.get(user_id=request.user.id)

        if request.method == 'GET':
            correct_incorrect_data_tuple = student.correct_incorrect_data_tuple
            return Response({'correct_incorrect_data_tuple': correct_incorrect_data_tuple})

        elif request.method == 'PUT':
            correct_incorrect_data = request.data.get('correct_incorrect_data_tuple')

            if correct_incorrect_data is not None:
                student.correct_incorrect_data_tuple = tuple(map(int, correct_incorrect_data.split(',')))
                student.save()
                return Response({'correct_incorrect_data_tuple': student.correct_incorrect_data_tuple})
            else:
                return Response({'error': 'Please provide valid data for correct_incorrect_data_tuple'},
                                status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def cards_read(self, request):
        student = Student.objects.get(user_id=request.user.id)
        
        if request.method == 'GET':
            # Return the current number of news cards read
            return Response({'cards_read': student.cards_read})
        
        elif request.method == 'PUT':
            # Update the number of news cards read from the request
            cards_read = request.data.get('cards_read')
            try:
                if cards_read is not None:
                    # Convert to integer and update
                    cards_read = int(cards_read)
                    student.cards_read = cards_read
                    student.save(update_fields=['cards_read'])
                    return Response({'cards_read': student.cards_read})
                else:
                    # If no valid number was provided, return an error response
                    return Response({'error': 'Please provide a valid number for cards_read'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                # Handle case where the provided value cannot be converted to an integer
                return Response({'error': 'Invalid input for cards_read, must be an integer'},
                                status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def student_accuracy_score (self, request):
        student = Student.objects.get(user_id=request.user.id)

        if request.method == 'GET':            
            accuracy_score = student.calculate_accuracy_score()  # Calculate accuracy score
            return Response({'accuracy_score': accuracy_score})

            
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def accuracy_scores(self, request):
        accuracy_scores = Student.objects.values_list('accuracy_score', flat=True)
        return Response(list(accuracy_scores))
        
    # @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    # def saved_questions(self, request):
    #     (student) = Student.objects.prefetch_related('saved_questions__subject').get(user_id=request.user.id)
    #     if request.method == 'GET':
    #         serializer = StudentSavedQuestionsSerializer(student)
    #         return Response(serializer.data) 
    #     elif request.method == 'PUT':
    #         serializer = StudentSerializer(student, data = request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)

class TrendingTopicsViewSet(ModelViewSet):
    queryset = Trending.objects.all()
    serializer_class = TrendingTopicsSerializer
    permission_classes = [IsAdminOrReadOnly] #change this and others to is Authenticated    

class BlogCardButtonViewSet(ModelViewSet):
    queryset = BlogCardButton.objects.all()
    serializer_class = BlogCardButtonSerializer
    permission_classes = [AllowAny]

class TrendingArchiveViewSet(ModelViewSet):
    queryset = TrendingArchive.objects.all()
    serializer_class = TrendingArchiveSerializer
    # permission_classes = [IsAdminOrReadOnly]    
    permission_classes = [IsAuthenticated]    

class TrendingArchiveViewSet(ModelViewSet):
    queryset = TrendingArchive.objects.all()
    serializer_class = TrendingArchiveSerializer
    permission_classes = [IsAdminOrReadOnly]    

class FLTCollectionViewSet(ModelViewSet):
    queryset = FLTCollection.objects.all()
    serializer_class = FLTCollectionSerializer
    # permission_classes = [IsAdminOrReadOnly]     change this before production
    
    


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