from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, ArticleListView

app_name = BlogConfig.name

urlpatterns = [
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('article/update/<int:pk>', ArticleUpdateView.as_view(), name='article_update'),
    path('article/delete/<int:pk>', ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/', ArticleListView.as_view(), name='articles'),
]