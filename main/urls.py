from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>', views.detail, name='detail'),
    path('comment/create/<int:article_id>', views.comment_create, name='comment_create'),
    path('article/create', views.article_create, name='article_create'),
]