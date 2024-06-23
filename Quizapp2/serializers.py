from rest_framework import serializers
from .models import Creamcard, QuizQuestion, QuizQuestionCollection, Student, Trending,TrendingArchive, FLTCollection, BlogCardButton, NotesCardsCollection, NotesCard, Subject
from drf_writable_nested.serializers import WritableNestedModelSerializer

class QuizQuestionSerializerSimple(serializers.ModelSerializer):
    # count = serializers.SerializerMethodField('get_count')
    class Meta:
        model = QuizQuestionCollection
        # fields = ['id','title','subject','count']
        fields = ['id','title','subject','created_at']
    
    # def get_count(self, obj):
    #     return QuizQuestionCollection.objects.all().count()

class FLTCollectionSerializer(serializers.ModelSerializer):
    tests = QuizQuestionSerializerSimple(many=True, read_only=True)
    class Meta:
        model = FLTCollection
        fields = ['id','title','description','tests','created_at']

class NotesCardSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.subject_name', read_only=True) 
    class Meta:
        model = NotesCard
        fields = ['id','subject', 'title', 'body']  # Adjust fields as per your requirement

class NotesCardsCollectionSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    notes_cards = NotesCardSerializer(many=True, read_only=True)  # Define the nested serializer for NotesCard
    class Meta:
        model = NotesCardsCollection
        fields = ['id', 'topic', 'subject', 'notes_cards']

class CreamCardsSerializer(serializers.ModelSerializer):
    related_notes_collection = NotesCardsCollectionSerializer(read_only=True)
    
    class Meta:
        model = Creamcard
        fields = ['id', 'created_at', 'subject', 'ImageURL', 'title', 'body', 'related_quiz', 'related_notes_collection']
    subject = serializers.StringRelatedField()

class CreamCardIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creamcard
        fields = ['id']

class BlogCardButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCardButton
        fields = ['ImageURL','title','body']

class TrendingTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trending
        fields = ['updated_at','topics']

class TrendingArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingArchive
        # fields = '__all__'
        fields = ['id','year','month','topics']

class QuizQuestionSerializers(serializers.ModelSerializer): #https://stackoverflow.com/a/33182227/3344514
    # collection = serializers.PrimaryKeyRelatedField(queryset=QuizQuestionCollection.objects.all(), many=True)
    class Meta:
        model = QuizQuestion
        fields = ['id','questionText','option_1','option_2','option_3','option_4','isACorrect',
        'isBCorrect','isCCorrect','isDCorrect','correctCount','inCorrectCount','explanation']

class QuizQuestionCollectionSerializers(serializers.ModelSerializer):  #https://stackoverflow.com/a/33182227/3344514
    class Meta:
        model = QuizQuestionCollection
        fields = ['created_at','id','collection_questions']
    
    collection_questions = QuizQuestionSerializers(many=True, read_only=True)




# class AccuracySerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Accuracy
#         fields = ['id','correct_attempt','incorrect_attempt']

# class AccuracySerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Accuracy
#         fields = ['id','correct_attempt','incorrect_attempt']

class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    # accuracy_score = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    # accuracy = AccuracySerializer()
    class Meta:
        model = Student
        # fields = ['id','user_id','date_joined','phone','birth_date','membership','saved_cards','accuracy_score','last_updated','correct_incorrect_data']
        fields = ['id','user_id','date_joined','phone','birth_date','membership','saved_cards','correct_incorrect_data', 'accuracy_score', 'cards_read']


class StudentAccuracySerializer(WritableNestedModelSerializer):
    # user_id = serializers.IntegerField(read_only=True)
    # accuracy = AccuracySerializer()
    class Meta:
        model = Student
        fields = ['id','user_id','accuracy']


#1
class SavedCreamCardsSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    class Meta:
        model = Creamcard
        fields = ['id','created_at','subject','ImageURL','title','body','related_quiz']

#2
class StudentSavedCardsPutSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Student
        fields = ['user_id','saved_cards']

#3
class StudentSavedCardsGetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    saved_cards = SavedCreamCardsSerializer(many=True)
    class Meta:
        model = Student
        fields = ['user_id','saved_cards']


# class StudentSavedQuestionsSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(read_only=True)
#     saved_questions = QuizQuestionSerializers(many=True)

#     class Meta:
#         model = Student
#         fields = ['user_id','saved_questions']

