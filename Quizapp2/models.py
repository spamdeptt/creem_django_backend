from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings

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
    created_at  = models.DateField(auto_now_add=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title

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

    def __str__(self):
        return f"{self.title}"

    class Meta:
         verbose_name_plural = "Cream Cards"

class Accuracy(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        return f"{self.user}"

    class Meta:
         verbose_name_plural = "Accuracy"


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
    # saved_questions = models.ManyToManyField(QuizQuestion,blank=True, related_name='saved_by')
    accuracy = models.ForeignKey(Accuracy, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)

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


