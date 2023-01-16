from django.contrib import admin
from django.db.models.aggregates import Count
from .models import QuizQuestionCollection, Author, Subject, Topic,Creamcard, QuizQuestion, Student, Accuracy, Trending, FLTCollection
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

admin.site.register(Author)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(FLTCollection)
# admin.site.register(Trending)


class CollectionInline(admin.TabularInline):
    model = QuizQuestion.collection.through


@admin.register(Creamcard)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('body',)
class CreamCardsAdmin(admin.ModelAdmin):
    list_display = ("created_at","title","subject")
    search_fields = ('title',)

@admin.register(Trending)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('topics',)
class TrendingAdmin(admin.ModelAdmin):
    list_display = ("updated_at","topics")


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display= ['preview_text','subject','id','get_collections']
    list_filter = ('subject','collection')
    list_display_links = ['preview_text']
    search_fields = ('preview_text',)
    list_select_related=['subject']
    
    def get_collections(self, instance):
        return [collection.title for collection in instance.collection.all()]
    
    def get_queryset(self, request):
        queryset = QuizQuestion.objects.prefetch_related('collection')
        return queryset


@admin.register(QuizQuestionCollection)
class QuizQuestionCollectionAdmin(admin.ModelAdmin):
    list_display= ['id','created_at','title']





#https://stackoverflow.com/questions/43894232/displaying-both-sides-of-a-manytomany-relationship-in-django-admin
# @admin.register(models.QuizQuestionCollection) 
# class QuizQuestionCollectionAdmin(admin.ModelAdmin):
#     list_display= ['title','id','created_at']
#     search_fields = ('title',)
#     list_display_links = ['title'] 
#     # model = models.QuizQuestionCollection
#     inlines=[
#         CollectionInline,
#     ]

@admin.register(Accuracy)
class AccuracyAdmin(admin.ModelAdmin):
    list_display = ['id','student','total','percentage']


@admin.register(Student)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','membership','date_joined']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         orders_count=Count('order')
    #     )

