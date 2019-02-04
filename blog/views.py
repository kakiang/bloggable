from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, FileResponse
from django.urls import reverse

import io
from reportlab.pdfgen import canvas

from .models import Post, Comment
from .forms import CommentForm, SearchForm, SharePostEmailForm
from django.views.decorators.http import require_POST
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    RedirectView
)
from django.views.generic.base import TemplateView
from django.db.models import Q
from taggit.models import Tag

def home(request):
    context = {
        "posts": Post.published.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'status', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'status', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    # ordering = ['-created']
    paginate_by = 3

    def get_context_data(self,**kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # context['search_form'] = SearchForm
        return context


class PostListViewByTag(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    # ordering = ['-created']
    paginate_by = 3

    def get_queryset(self):
        qs = super(PostListViewByTag,self).get_queryset()
        self.tag = get_object_or_404(Tag,slug=self.kwargs.get('tag_slug'))
        return qs.filter(tags__in=[self.tag])

    def get_context_data(self,**kwargs):
        context=super(PostListViewByTag,self).get_context_data(**kwargs)
        context['tag']=self.tag
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        qs = super(UserPostListView, self).get_queryset()
        self.user = get_object_or_404(User,username=self.kwargs.get('username'))
        return qs.filter(author=self.user).order_by('-publish')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.user
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDisplayView(DetailView):
    model = Post
    query_pk_and_slug=True

    def get_object(self):
        object = super(PostDisplayView, self).get_object()
        object.view_count += 1
        object.save(update_fields=['view_count'])
        return object

    def get_context_data(self, **kwargs):
        context = super(PostDisplayView,self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        context['comment_form'] = CommentForm
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    # model = Comment
    # fields = ['content',]
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        print(form.is_valid)
        form.instance.author = self.request.user
        post = Post.objects.get(slug=self.kwargs['slug'])
        form.instance.post = post
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug':self.kwargs['slug']})


class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PostDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)


class SearchPostView(TemplateView):

    template_name = 'blog/home.html'

    def get_context_data(self,**kwargs):
        term = self.request.GET.get('term',None)
        # print("term:{}".format(term))
        context=super().get_context_data(term=term, **kwargs)
        if term:
            posts=Post.published.all().filter(Q(content__icontains=term) | Q(title__icontains=term))
            context['posts']=posts
            # print(posts.count)
        # context['search_form']=SearchForm
        context['search']=term
        return context


def post_share_email(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == 'POST':
        form = SharePostEmailForm(request.POST)

        if form.is_valid():
            mail=form.cleaned_data()
            post_url=request.build_absolute_url(post.get_absolute_url())
            subject='{}({}) recommends you reading "{}"'.format(mail['name'],mail['sender'],post.title)
            message=mail['message']
            name=mail['name']
            sender=mail['sender']
            recipient=mail['recipient']
    else:
        form = SharePostEmailForm(sender=request.user.email, name=request.user.first_name)

    return render(request, 'blog/share.html',)

class PostLikeViewRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        print(slug)
        object = get_object_or_404(Post,slug=slug)
        url_ = object.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in object.users_clap.all():
                object.users_clap.remove(user)
            else:
                object.users_clap.add(user)
        return url_

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get('slug')
        object = get_object_or_404(Post,slug=slug)
        url_ = object.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in object.users_clap.all():
                liked = True
                object.users_clap.remove(user)
            else:
                liked = False
                object.users_clap.add(user)
        data = {
            'updated':updated,
            'liked':liked
        }
        return Response(data)

def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    print('post_like')
    if post_id and action:
        print('id={}, action={}'.format(post_id,action))
        try:
            post = Post.objects.get(pk=post_id)
            if action == 'like':
                print('like action')
                post.users_clap.add(request.user)
            else:
                print('unlike action')
                post.users_clap.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})


# from django.conf import settings
# from django.template.loader import render_to_string
# import weasyprint
#
# # @staff_member_required
# def post_pdf(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     html = render_to_string('blog/pdf.html', {'object': post})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="{}.pdf"'.format(post.slug)
#     weasyprint.HTML(string=html).write_pdf(response,
#     stylesheets=[weasyprint.CSS('blog/static/blog/css/bootstrap.min.css')])
#     return response


def view_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
