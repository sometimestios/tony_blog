from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Post, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.views.generic import ListView
import markdown
import re


# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10


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
    post.increase_views()
    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, name=self.kwargs.get('category_name'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, name=self.kwargs.get('tag_name'))
        return super(TagView, self).get_queryset().filter(tag=tag)


def tag(request, tag_name):
    tag_class = Tag.objects.get(name=tag_name)
    post_list = Post.objects.filter(tag=tag_class)
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })

# def page_guide(request):
#     all_post = Post.objects.all()
#     paginator = Paginator(all_post, 10)
#     page_num = request.GET.get('page')
#     try:
#         post_list = paginator.page(page_num)
#     except(PageNotAnInteger, EmptyPage, InvalidPage):
#         post_list = paginator.page('1')
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
#     })
