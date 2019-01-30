from django import template
register = template.Library()
from ..models import Post

@register.inclusion_tag('blog/latest_posts.html')
def display_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}
