from rest_framework import serializers
from .models import CreamCards, QuizQuestion, QuizQuestionCollection



class CreamCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreamCards
        fields = '__all__'
        # fields = ['id','created_at','author','subject','ImageURL','title','body','related_quiz']

    def to_representation(self, instance):
        rep = super(CreamCardsSerializer, self).to_representation(instance)
        rep['subject'] = instance.subject.subject_name
        return rep



class QuizQuestionSerializers(serializers.ModelSerializer): #https://stackoverflow.com/a/33182227/3344514
    collection = serializers.PrimaryKeyRelatedField(queryset=QuizQuestionCollection.objects.all(), many=True)
    class Meta:
        model = QuizQuestion
        fields = ['id','collection','questionText','option_1','option_2','option_3','option_4','isACorrect',
        'isBCorrect','isCCorrect','isDCorrect','correctCount','inCorrectCount','explanation']
        # fields = '__all__'
    
    

class QuizQuestionCollectionSerializers(serializers.ModelSerializer):  #https://stackoverflow.com/a/33182227/3344514
    collection_questions = QuizQuestionSerializers(many=True, read_only=True)
    class Meta:
        model = QuizQuestionCollection
        fields = '__all__'