from django import template
from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html')
def show_recent_posts(num=5):
    return {
        'recent_post_list': Post.objects.all()[:num],
    }


@register.inclusion_tag('blog/inclusions/_archive.html')
def show_archive():
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/inclusions/_category.html')
def show_category():
    return {
        'category_list': Category.objects.all()
    }


@register.inclusion_tag('blog/inclusions/_tag.html')
def show_tag():
    return {
        'tag_list':Tag.objects.all()
    }
