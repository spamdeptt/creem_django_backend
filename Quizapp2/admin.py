from django.contrib import admin
from .models import QuizQuestionCollection, Authors, Subjects, Topic,CreamCards, QuizQuestion, Customer
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

admin.site.register(Authors)
admin.site.register(Subjects)
admin.site.register(Topic)

class CollectionInline(admin.TabularInline):
    model = QuizQuestion.collection.through


@admin.register(CreamCards)
class SummerAdmin(SummernoteModelAdmin): 
    summernote_fields = ('body',)
class CreamCardsAdmin(admin.ModelAdmin):
    list_display = ("created_at","title","subject")
    search_fields = ('title',)



@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display= ['preview_text','subject','id','get_collections']
    list_filter = ('subject', )
    list_display_links = ['preview_text']
    search_fields = ('preview_text',)
    
    def get_collections(self, instance):
        return [collection.title for collection in instance.collection.all()]


admin.site.register(QuizQuestionCollection)


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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         orders_count=Count('order')
    #     )
