from rest_framework import serializers
from .models import CreamCards, QuizQuestion, QuizQuestionCollection



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
        # fields = '__all__'

class QuizQuestionCollectionSerializers(serializers.ModelSerializer):  #https://stackoverflow.com/a/33182227/3344514
    class Meta:
        model = QuizQuestionCollection
        fields = ['id','collection_questions']
        # fields = '__all__'
    
    collection_questions = QuizQuestionSerializers(many=True, read_only=True)