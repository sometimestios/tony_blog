from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.urls import reverse
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import re
from django.utils.functional import cached_property


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}


# Create your models here.

# 所有模型都要继承models.Model以获得模型方法
class Category(models.Model):
    name = models.CharField(max_length=20)

    # 通过内部类Meta可以修改后台显示的名称
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    # Python的魔术方法，在查询时显示name属性，不需要调用.name属性
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=40)  # 等价于关键词参数verbose_name='标题'
    created_time = models.DateTimeField('创建时间', default=timezone.now)  # 默认值为当前时间，timezone.now可以自适应时区
    modified_time = models.DateTimeField('修改时间')
    body = models.TextField('正文')
    excerpt = models.TextField('摘要', max_length=300, blank=True)  # 允许为空
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)  # 多对一关联；级联删除的策略
    tag = models.ManyToManyField(Tag, verbose_name='标签')  # 多对多
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE, blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_time', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:250]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # reverse函数找到blog应用的urlpatterns中，名为detail的url，并传入kwargs中的参数，返回这个url
        # 通过这种解析url的方式，使得url与视图函数的绑定更加灵活，实现了url与模型实例的关联
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)
