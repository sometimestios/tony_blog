from django.contrib import admin
from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_time']


# Register your models here.
admin.site.register(Comment,CommentAdmin)
