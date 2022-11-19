from rest_framework import serializers
from .models import CreamCards, QuizQuestion

class CreamCardsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreamCards
        fields = '__all__'
        # fields = ['id','created_at','author','subject','url','title','body','html', 'plain']

    def to_representation(self, instance):
        rep = super(CreamCardsSerializer, self).to_representation(instance)
        rep['subject'] = instance.subject.subject_name
        return rep



class QuizQuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = '__all__'