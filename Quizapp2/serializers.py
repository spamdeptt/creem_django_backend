from rest_framework import serializers
from .models import CreamCards, QuizQuestion, QuizQuestionCollection

class CreamCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreamCards
        fields = '__all__'
        # fields = ['id','created_at','author','subject','url','title','body','html', 'plain']

    def to_representation(self, instance):
        rep = super(CreamCardsSerializer, self).to_representation(instance)
        rep['subject'] = instance.subject.subject_name
        return rep



class QuizQuestionSerializers(serializers.ModelSerializer): #https://stackoverflow.com/a/33182227/3344514
    collection = serializers.PrimaryKeyRelatedField(queryset=QuizQuestionCollection.objects.all(), many=True)
    class Meta:
        model = QuizQuestion
        fields = '__all__'


class QuizQuestionCollectionSerializers(serializers.ModelSerializer):  #https://stackoverflow.com/a/33182227/3344514
    collection_questions = QuizQuestionSerializers(many=True, read_only=True)
    class Meta:
        model = QuizQuestionCollection
        fields = '__all__'