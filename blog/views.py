from django.shortcuts import render, get_object_or_404
from .models import Post
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
    # 通过markdown函数将md语法的正文转成了html文本
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={
        'post': post
    })
