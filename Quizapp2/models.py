from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone



class Author(models.Model):
    author_name = models.CharField(max_length=255)

    def __str__ (self):
        return self.author_name
    
    class Meta:
         verbose_name_plural = "Authors"

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name

    class Meta:
         verbose_name_plural = "Subjects"

class Topic(models.Model):
    subject  = models.ForeignKey(Subject, models.CASCADE, null=True, blank=True, related_name="topics")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"({self.subject})-{self.name}"

class QuizQuestionCollection(models.Model):
    created_at  = models.DateField(default=timezone.now)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255,blank=True, null=True)
    def __str__(self):
        return self.title
    
    def question_count(self):
        return self.collection_questions.count()  # Use the related_name defined earlier in NotesCard model
    question_count.short_description = 'Quiz Questions Count'

class NotesCardsCollection(models.Model):
    created_at  = models.DateField(default=timezone.now)
    topic = models.CharField(max_length=255,blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True )
    
    def __str__(self):
        return self.topic
    
    def notes_count(self):
        return self.notes_cards.count()  # Use the related_name defined earlier in NotesCard model
    notes_count.short_description = 'Notes Count'

class FLTCollection(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tests = models.ManyToManyField(QuizQuestionCollection)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name_plural = "FLT Collections"

class QuizQuestion(models.Model):
    created_at  = models.DateTimeField(null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    collection = models.ManyToManyField(QuizQuestionCollection, blank=True, related_name="collection_questions" )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    preview_text = models.CharField(max_length=255)
    questionText = models.TextField()
    option_1 = models.CharField(max_length=510)
    option_2 = models.CharField(max_length=510)
    option_3 = models.CharField(max_length=510)
    option_4 = models.CharField(max_length=510)
    isACorrect = models.BooleanField(default=False)
    isBCorrect = models.BooleanField(default=False)
    isCCorrect = models.BooleanField(default=False)
    isDCorrect = models.BooleanField(default=False)
    correctCount = models.IntegerField(default=1, blank=True, null=True)
    inCorrectCount = models.IntegerField(default=1, blank=True, null=True)
    explanation = models.TextField()

    def __str__ (self):
        return f"({self.subject})-{self.preview_text}"

    class Meta:
         verbose_name_plural = "Quiz Questions"
         ordering = ['subject']

class Creamcard(models.Model):
    created_at  = models.DateTimeField(null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True )
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True )
    ImageURL = models.CharField(max_length=1500)
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True, null=True)
    related_quiz = models.ForeignKey(QuizQuestionCollection, on_delete=models.SET_NULL,null=True, blank=True)
    related_notes_collection = models.ForeignKey(NotesCardsCollection, on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
         verbose_name_plural = "Cream Cards"

# HOW TO USE THE RELATED NAME TO access the NotesCard objects related to a NotesCardsCollection instance 
# notes_collection = NotesCardsCollection.objects.get(id=1)
# related_notes = notes_collection.notes_cards.all()
class NotesCard(models.Model):
    created_at  = models.DateTimeField(null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True )
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    collection = models.ManyToManyField(NotesCardsCollection, blank=True, related_name="notes_cards" )

    def __str__(self):
        return f"{self.title}"

    class Meta:
         verbose_name_plural = "NotesCards"


class BlogCardButton(models.Model):
    created_at  = models.DateTimeField(null=True)
    ImageURL = models.CharField(max_length=1500)
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
         verbose_name_plural = "Blog Button Card"

class Student(models.Model):
    MEMBERSHIP_PREMIUM = 'P'
    MEMBERSHIP_FREE = 'F'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_PREMIUM, 'Premium'),
        (MEMBERSHIP_FREE, 'Free'),
    ]
    phone = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_FREE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saved_cards = models.ManyToManyField(Creamcard,blank=True, related_name='saved_by')
    # saved_questions = mode  ls.ManyToManyField(QuizQuestion,blank=True, related_name='saved_by')
    # accuracy = models.ForeignKey(Accuracy, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # questions_attempted = models.PositiveIntegerField()
    # accuracy_score = models.DecimalField(max_digits=5, decimal_places=2)  # Example: 99.50
    # last_updated = models.DateTimeField(default=timezone.now,blank=True, null=True)
    # correct_attempts_count = models.PositiveIntegerField(default=0)
    # incorrect_attempts_count = models.PositiveIntegerField(default=0)
    correct_incorrect_data = models.CharField(max_length=20, default='1,2,3')  # Adjust max_length as per your requirement
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cards_read = models.PositiveIntegerField(default=0)


    def calculate_accuracy_score(self):
        correct, incorrect, total_attempts = map(int, self.correct_incorrect_data.split(','))

        if total_attempts > 0:
            # Calculate the simple accuracy ratio (correct attempts / total attempts)
            simple_ratio = correct / (correct + incorrect)
            # Calculate the ratio of attempted questions to total questions attempted
            total_ratio = (correct + incorrect) / total_attempts
            # Adjust the accuracy score by multiplying the simple ratio by the total ratio
            accuracy = simple_ratio * total_ratio * 100
        else:
            accuracy = 0
        
        accuracy = round(accuracy, 2)
        return accuracy
    
    # def calculate_accuracy_score(self):
    #     data_parts = self.correct_incorrect_data.split(',')
    #     correct = int(data_parts[0])
    #     incorrect = int(data_parts[1])
    #     # correct, incorrect = map(int, self.correct_incorrect_data.split(','))
    #     total_attempts = correct + incorrect
    #     if total_attempts > 0:
    #         accuracy = (correct / total_attempts) * 100
    #     else:
    #         accuracy = 0
    #     accuracy = round(accuracy, 2)
    #     return accuracy


    def accuracy_score_changed(self):
        return self.pk is None or self.accuracy_score != self.__class__.objects.get(pk=self.pk).accuracy_score

    def get_correct_incorrect_data_as_tuple(self):
        """
        This method converts the stored string to a tuple of integers.
        """
        if self.correct_incorrect_data:
            return tuple(map(int, self.correct_incorrect_data.split(',')))
        else:
            return None

    def set_correct_incorrect_data_as_tuple(self, coord_tuple):
        """
        This method converts the tuple of integers to a string and saves it.
        """
        self.correct_incorrect_data = ','.join(map(str, coord_tuple))

    correct_incorrect_data_tuple = property(get_correct_incorrect_data_as_tuple, set_correct_incorrect_data_as_tuple)


    def save(self, *args, **kwargs):
        if not self.accuracy_score_changed():
            self.accuracy_score = self.calculate_accuracy_score()
        super().save(*args, **kwargs)

    # def accuracy_score_changed(self):
    #     return self.pk is None or self.accuracy_score != self.__class__.objects.get(pk=self.pk).accuracy_score
    
    def accuracy_score_changed(self):
        return self.pk is None or self.accuracy_score != self.__class__.objects.get(pk=self.pk).accuracy_score

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        # permissions =[('view_history','Can view history')]

class Accuracy(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student = models.OneToOneField(Student,on_delete=models.CASCADE, blank=True, null=True)
    correct_attempt = models.IntegerField(default=1)
    incorrect_attempt = models.IntegerField(default=1)
    total = models.IntegerField(default=2)
    percentage = models.DecimalField(decimal_places=2, max_digits=10, default=50)

    @property
    def get_total(self):
        return self.correct_attempt + self.incorrect_attempt

    @property
    def get_percentage(self):
        return (self.correct_attempt/(self.correct_attempt+self.incorrect_attempt))*100

    def save(self, *args, **kwargs):
        self.percentage = self.get_percentage
        self.total = self.get_total
        super(Accuracy, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student}"

    class Meta:
         verbose_name_plural = "Accuracy"


class Trending(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    topics = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.updated_at}"
    
    class Meta:
         verbose_name_plural = "Trending Topics"


class TrendingArchive(models.Model):
    JANUARY ='JAN'
    FEBRUARY = 'FEB'
    MARCH = 'MAR'
    APRIL = 'APR'
    MAY = 'MAY'
    JUNE = 'JUN'
    JULY = 'JUL'
    AUGUST = 'AUG'
    SEPTEMBER = 'SEP'
    OCTOBER = 'OCT'
    NOVEMBER = 'NOV'
    # MONTH_CHOICES = [
    #     ('JAN', 'January'),
    #     ('FEB', 'February'),
    #     ('MAR', 'March'),
    #     ('APR', 'April'),
    #     ('MAY', 'May'),
    #     ('JUN', 'June'),
    #     ('JUL', 'July'),
    #     ('AUG', 'August'),
    #     ('SEP', 'September'),
    #     ('OCT', 'October'),
    #     ('NOV', 'November'),
    #     ('DEC', 'December'),
    # ]
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    YEAR_CHOICES = [
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
    ]
    created_at  = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    year = models.CharField(choices=YEAR_CHOICES, default=2023, max_length=4)
    month = models.CharField(choices=MONTH_CHOICES, max_length=12)
    topics = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.month} {self.year}"

    class Meta:
         verbose_name_plural = "Trending Topics Archives"
         ordering = ['-created_at']
    