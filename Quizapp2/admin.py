from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


admin.site.register(models.Authors)
admin.site.register(models.Subjects)
admin.site.register(models.QuizQuestion)
admin.site.register(models.Topic)
admin.site.register(models.QuizQuestionCollection)

@admin.register(models.CreamCards)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('body',)
class CreamCardsAdmin(admin.ModelAdmin):
    list_display = ("created_at","title","subject")





