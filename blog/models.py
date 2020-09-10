from django.db import models
from django.contrib.auth.admin import User
# Create your models here.

# 所有模型都要继承models.Model以获得模型方法
class Category(models.Model):
    name=models.CharField(max_length=20)

class Tag(models.Model):
    name=models.CharField(max_length=20)

class Post(models.Model):
    title=models.CharField(max_length=40)
    createdTime=models.DateTimeField()
    modifiedTime=models.DateTimeField()
    body=models.TextField()
    excerpt=models.TextField(max_length=400,blank=True)  # 允许为空
    category=models.ForeignKey(Category,on_delete=models.CASCADE)  # 多对一关联；级联删除的策略
    tag=models.ManyToManyField(Tag)  # 多对多
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)