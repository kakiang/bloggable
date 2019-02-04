from django import template
register = template.Library()
from ..models import Post

from django.db.models import Count

@register.inclusion_tag('blog/latest_posts.html')
def display_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'posts':latest_posts}


@register.inclusion_tag('blog/latest_posts.html')
def most_commented_posts(count=5):
    c_posts = Post.published.annotate(comments=Count('comment')).order_by('-comments')[:count]
    # latest_posts = Post.published.order_by('-updated')[:count]
    return {'posts':c_posts}


@register.inclusion_tag('blog/latest_posts.html')
def most_clapped_posts(count=5):
    latest_posts = Post.published.annotate(claps=Count('users_clap')).order_by('-claps')[:count]
    # latest_posts = Post.published.order_by('-updated')[:count]
    return {'posts':latest_posts}
