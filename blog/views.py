from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown


# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-createdTime')
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 通过markdown函数将md语法的正文转成了html文本
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return render(request, 'blog/detail.html', context={
        'post': post
    })
