from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from tinymce import HTMLField

from .utils import get_read_time

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

# class UserPostsManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager,self).get_queryset().filter(status='published')


class SearchManager(models.Manager):
    def search(self, **kwargs):
        # self.get_queryset()
        qs = super(SearchManager,self).get_queryset()
        if kwargs.get('term', ''):
            qs = qs.filter(content__icontains=kwargs['term'])
        return qs


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # content = models.TextField()
    content = HTMLField('content')
    # We specify the name of the reverse relationship, from User to Post
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    read_time = models.TimeField(null=True, blank=True)
    users_clap = models.ManyToManyField(User, related_name='posts_liked', blank=True)
    view_count = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)

    objects = models.Manager()
    published = PublishedManager()
    searchManager = SearchManager()

    def read_time_min(self):
        print(self.read_time)
        return self.read_time

    def claps_count(self):
        return self.users_clap.count()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'year': self.publish.year,
                                              'month': self.publish.strftime('%m'),
                                              'day': self.publish.strftime('%d'),
                                              'slug': self.slug})

    def get_clap_url(self):
        return reverse('post-clap', kwargs={'year':self.publish.year,
                                            'month': self.publish.strftime('%m'),
                                            'day':self.publish.strftime('%d'),
                                            'slug':self.slug})

    def get_clap_api_url(self):
        return reverse('post-api-clap', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.content:
            self.read_time = get_read_time(self.content)
        super(Post, self).save(*args, **kwargs)


# def pre_save_post_receiver(instance, *args, **kwargs):
#     if instance.content:
#         instance.read_time = get_read_time(instance.content)
#
#
# pre_save.connect(pre_save_post_receiver, sender=Post)


class Comment(models.Model):
    # commentator_name = models.CharField(max_length=42)
    # commentator_email = models.EmailField(max_length=75)
    content = models.TextField(blank=False)
    # content = HTMLField('content')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='blog_comments', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'year': self.post.publish.year,
                                              'month': self.post.publish.strftime('%m'),
                                              'day': self.post.publish.strftime('%d'),
                                              'slug': self.post.slug})
