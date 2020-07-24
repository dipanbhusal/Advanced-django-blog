from django.shortcuts import render , reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .forms import PostForm
from .models import Post
# Create your views here.


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'

class PostCreateView(LoginRequiredMixin,CreateView):

    form_class = PostForm
    template_name = 'blog/post_create.html' 

    def form_valid(self, PostForm):
        
        objects = PostForm.save(commit=False)
        objects.author = self.request.user 
        objects.save()

        return super(PostCreateView, self).form_valid(PostForm)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'          

    def test_func(self):
        post_detail = self.get_object()
        if post_detail.author != self.request.user:
            return False
        return True


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user != post.author:
            return False
        return True



