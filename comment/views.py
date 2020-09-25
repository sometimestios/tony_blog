from blog.models import Post
from .forms import CommentForm
from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
# Create your views here.
@require_POST
def comment(request,post_pk):
    post=get_object_or_404(Post,pk=post_pk)
    form=CommentForm(request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
        messages.add_message(request,messages.SUCCESS,'评论成功',extra_tags='success')
        return redirect(post)
    else:
        messages.add_message(request, messages.ERROR, '评论发表失败，请检查表单格式', extra_tags='danger')
        context={
            'post':post,
            'form':form,
        }
    return render(request,'comment/preview.html',context=context)