from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Post, Category, Tag
import markdown
import re


# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-createdTime')
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(createdTime__year=year,
                                    createdTime__month=month).order_by('-createdTime')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def category(request, category_name):
    category_class = Category.objects.get(name=category_name)
    post_list = Post.objects.filter(category=category_class).order_by('-createdTime')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def tag(request, tag_name):
    tag_class = Tag.objects.get(name=tag_name)
    post_list = Post.objects.filter(tag=tag_class).order_by('-createdTime')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })
