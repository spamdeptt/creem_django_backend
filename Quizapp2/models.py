from django.db import models
from django.contrib.auth.models import User

class Authors(models.Model):
    author_name = models.CharField(max_length=255)

    def __str__ (self):
        return self.author_name
    
    class Meta:
         verbose_name_plural = "Authors"

class Subjects(models.Model):
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name

    class Meta:
         verbose_name_plural = "Subjects"

class Topic(models.Model):
    subject  = models.ForeignKey(Subjects, models.CASCADE, null=True, blank=True, related_name="topics")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"({self.subject})-{self.name}"

class CreamCards(models.Model):
    created_at  = models.DateTimeField(null=True)
    author = models.ForeignKey(Authors, models.SET_NULL, null=True, blank=True )
    subject = models.ForeignKey(Subjects, models.SET_NULL, null=True, blank=True )
    ImageURL = models.CharField(max_length=1500)
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
         verbose_name_plural = "Cream Cards"


class QuizQuestionCollection(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    created_at  = models.DateTimeField(null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True, related_name="quiz_questions")
    collection = models.ManyToManyField(QuizQuestionCollection, blank=True, related_name="collection_questions" )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, related_name="quiz_questions")
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
    explanation = models.TextField()

    def __str__ (self):
        return f"({self.subject})-{self.preview_text}"

    class Meta:
         verbose_name_plural = "Quiz Questions"
         ordering = ['subject']


class CreamCardsTest(models.Model):    
    created_at  = models.DateTimeField(null=True)
    author = models.ForeignKey(Authors, models.SET_NULL, null=True, blank=True )
    subject = models.ForeignKey(Subjects, models.SET_NULL, null=True, blank=True )
    url = models.CharField(max_length=1500, null=True, blank=True)
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
         verbose_name_plural = "Cream Cards Test"




