from django.contrib import admin
from django.db.models.aggregates import Count
from .models import QuizQuestionCollection, Author,NotesCardsCollection, Subject, Topic,Creamcard,NotesCard, QuizQuestion, Student, Accuracy, Trending, FLTCollection, TrendingArchive, BlogCardButton
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

admin.site.register(Author)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(TrendingArchive)
admin.site.register(BlogCardButton)
# admin.site.register(FLTCollection)
# admin.site.register(Trending)
admin.site.register(FLTCollection)

class CollectionInline(admin.TabularInline):
    model = QuizQuestion.collection.through


@admin.register(Creamcard)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('body',)
class CreamCardsAdmin(admin.ModelAdmin):
    list_display = ("created_at","title","subject")
    search_fields = ('title',)

@admin.register(NotesCard)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('body',)
class NotesCardsAdmin(admin.ModelAdmin):
    list_display = ("created_at","title","subject")
    search_fields = ('title',)

@admin.register(Trending)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('topics',)
class TrendingAdmin(admin.ModelAdmin):
    list_display = ("updated_at","topics")

# @admin.register(TrendingArchive)
# class SummerAdmin(SummernoteModelAdmin): 
#     summernote_fields = ('topics',)
# class TrendingArchiveAdmin(admin.ModelAdmin):
#     list_display = ("updated_at","topics")


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
    list_display= ['title','question_count','created_at']
        
    fieldsets = (
        (None, {
            'fields': ('created_at', 'title', 'subject'),
            'description': 'Make sure there is aleast one quiz question associated with QQC, else it breaks the app.'
        }),
    )

class NotesCardInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = NotesCard.collection.through  # Use the through model for the ManyToMany relationship
    extra = 1  # Number of extra forms to display

@admin.register(NotesCardsCollection)
class NotesCardsCollectionAdmin(admin.ModelAdmin):
    list_display= ['topic', 'subject', 'created_at', 'notes_count']
        
    fieldsets = (
        (None, {
            'fields': ('topic', 'subject', 'created_at'),
            'description': 'Make sure there is aleast one NoteCard associated with NCC, else it breaks the app.'
        }),
    )
    inlines = [NotesCardInline]
    





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

