from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

admin.site.register(models.Authors)
admin.site.register(models.Subjects)
admin.site.register(models.Topic)

class CollectionInline(admin.TabularInline):
    model = models.QuizQuestion.collection.through


@admin.register(models.CreamCards)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('body',)
class CreamCardsAdmin(admin.ModelAdmin):
    list_display = ("created_at","title","subject")
    search_fields = ('title',)



@admin.register(models.QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display= ['preview_text','subject','id','get_collections']
    list_filter = ('subject', )
    list_display_links = ['preview_text']
    search_fields = ('preview_text',)
    
    def get_collections(self, instance):
        return [collection.title for collection in instance.collection.all()]


@admin.register(models.QuizQuestionCollection) #https://stackoverflow.com/questions/43894232/displaying-both-sides-of-a-manytomany-relationship-in-django-admin
class QuizQuestionCollectionAdmin(admin.ModelAdmin):
    list_display= ['title','id','created_at']
    search_fields = ('title',)
    list_display_links = ['title']
    # model = models.QuizQuestionCollection //this was removed and nothing happended so it was left removed
    inlines=[
        CollectionInline,
    ]



