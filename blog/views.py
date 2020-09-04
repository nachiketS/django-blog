from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import urls
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# Create your views here.


data={
    'blogs':Post.objects.all(),
    'title':'home'
}

def home(request):
    return render(request,'blog/home.html',data)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date')

class PostListView(ListView):#generic views provided by django, list view used for populating lists apparently.
    model = Post
    template_name = 'blog/home.html' #changing the default template from blog/post_list.html i.e. <app>/<model>_<viewtype.html>
    context_object_name = 'blogs' #the variable name that is expected to be received by the template
    ordering = ['-date'] #sorting by dates descending
    paginate_by = 5

#Detail view used for rendering the actual posts one at a time.
class PostDetailView(DetailView): #this detail view looks for a template blog/post_detail.html
    model = Post

# @login_required can't use this bc it's a decorator and can't be used on classes
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super(). form_valid(form)
    success_url = reverse_lazy('blog-home')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super(). form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'blog/about.html',{'title':'about'})

