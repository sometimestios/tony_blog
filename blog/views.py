from django.shortcuts import render
from .models import Post
# Create your views here.
def index(request):
    post_list=Post.objects.all().order_by('-createdTime')
    return render(request,'index.html',context={
        'post_list':post_list,
    })

def detail(request,pk):
    return render(request,'blog/detail.html',context={
        'pk':pk
    })