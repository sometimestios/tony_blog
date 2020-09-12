from django.contrib import admin
from .models import Category, Tag, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'createdTime', 'modifiedTime', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category','tag']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


# Register your models here.

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)  # PostAdmin和Post关联起来
admin.site.register(Category)
