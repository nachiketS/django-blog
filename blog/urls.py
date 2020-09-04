from django.urls import path,include
from . import views
from . views import PostListView,PostDetailView, PostDeleteView

urlpatterns = [
    path('',views.PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>',views.UserPostListView.as_view(), name = 'blog-user-post'),
    path('post/<int:pk>/',views.PostDetailView.as_view(), name = 'post-detail'), #using pk as it is the default name that django expects. pk stands here for primary_key
    path('post/new',views.PostCreateView.as_view(),name = 'post-create'),#this expects a template blog/post_form.html
    path('post/<int:pk>/update/',views.PostUpdateView.as_view(),name = 'post-update'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name = 'post-delete'),
    path('about/',views.about, name = 'blog-about')
]
    