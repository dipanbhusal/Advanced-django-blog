from django.urls import path 
from .views import PostListView, PostCreateView, PostUpdateView, PostDetailView, PostDeleteView
app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('create/', PostCreateView.as_view(), name = 'post-create'),
    path('update/<slug:slug>/', PostUpdateView.as_view(), name = 'post-update'),
    path('<slug:slug>/', PostDetailView.as_view(), name = 'post-detail'),
    path('<slug:slug>/delete', PostDeleteView.as_view(), name = 'post-delete'),
]