from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comment/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('comment/inclusions/_comment_list.html', takes_context=True)
def show_comment_list(context, post):
    comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_count': comment_count,
    }
