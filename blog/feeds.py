from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

from .models import Post

class LatestPostsFeed(Feed):
    title = 'Bloggable'
    link = ''
    description = 'Latest posts of Bloggable'

    def items(self):
        return Post.published.all()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(strip_tags(item.content),60)
