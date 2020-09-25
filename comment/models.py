from django.db import models
from blog.models import Post
from django.utils import timezone
# Create your models here.

class Comment(models.Model):
    name=models.CharField('阁下大名',max_length=20)
    email=models.EmailField('邮箱')
    text=models.TextField('评论',max_length=400)
    created_time=models.DateTimeField('创建时间',default=timezone.now)
    post=models.ForeignKey(Post,verbose_name='文章',on_delete=models.CASCADE)

    class Meta:
        verbose_name='评论'
        verbose_name_plural=verbose_name
        ordering=['-created_time','name']


    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])
