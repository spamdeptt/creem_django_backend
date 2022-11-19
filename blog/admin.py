from django.contrib import admin
from blog.models import Posts,Category


@admin.register(Posts)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['title','id','status','slug','author']
    prepopulated_fields = {'slug':('title',), }


admin.site.register(Category)


