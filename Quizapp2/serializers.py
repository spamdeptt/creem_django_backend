from rest_framework import serializers
from .models import CreamCards, QuizQuestion, QuizQuestionCollection, Student


class CreamCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreamCards
        fields = ['id','created_at','subject','ImageURL','title','body','related_quiz']
    
    # author = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()

class QuizQuestionSerializers(serializers.ModelSerializer): #https://stackoverflow.com/a/33182227/3344514
    # collection = serializers.PrimaryKeyRelatedField(queryset=QuizQuestionCollection.objects.all(), many=True)
    class Meta:
        model = QuizQuestion
        fields = ['id','questionText','option_1','option_2','option_3','option_4','isACorrect',
        'isBCorrect','isCCorrect','isDCorrect','correctCount','inCorrectCount','explanation']

class QuizQuestionCollectionSerializers(serializers.ModelSerializer):  #https://stackoverflow.com/a/33182227/3344514
    class Meta:
        model = QuizQuestionCollection
        fields = ['id','collection_questions']
    
    collection_questions = QuizQuestionSerializers(many=True, read_only=True)


class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Student
        fields = ['id','user_id','phone','birth_date','membership']