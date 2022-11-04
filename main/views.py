import main.models as models
from bs4 import BeautifulSoup
from time import time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls.base import reverse
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required

PER_PAGE_NUM = 20

def index(request):
    board_type = request.GET.get('board', 'FR')
    page = request.GET.get('page', '1')
    
    # Get Article objects
    try:
        objects = models.Article.objects.filter(board_type=board_type).order_by('-create_date')
        board_name = models.Article.BoardType[board_type].label
    except:  # 존재하지 않는 borad_type인 경우
        objects = None
        board_name = '존재하지 않는 게시판입니다.'

    if objects is not None:
        total_article_length = len(objects)
        paginator = Paginator(objects, PER_PAGE_NUM)
        objects = paginator.get_page(page)

    context = {
        'article_list': objects,
        'board_name': board_name, 
        'board_type': board_type,
        'start_idx': total_article_length - objects.end_index() + 1 if objects is not None else -1,
    }

    return render(request, 'main/index.html', context)

def detail(request, article_id):
    article = get_object_or_404(models.Article, id=article_id)

    context = {
        'article': article,
        'comment_list': article.comment_set.all(),
    }

    return render(request, 'main/detail.html', context)

@login_required(login_url='common:login')
def comment_create(request, article_id):
    article = get_object_or_404(models.Article, id=article_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.save()
    else:
        form = CommentForm()

    context = {
        'article': article,
        'comment_list': article.comment_set.all(),
        'form': form,
    }

    return render(request, 'main/detail.html', context)

@login_required(login_url='common:login')
def article_create(request):
    if request.method == 'POST':
        board_type = request.POST.get('board_type')
        form = ArticleForm(request.POST)

        if form.is_valid():
            # Article 저장
            article = form.save(commit=False)
            article.user = request.user
            article.create_date = timezone.now()
            article.save()

            # django-summernote 업로드 이미지경로 저장
            img_src_list = get_img_src_from_html(article.content)
            for img_src in img_src_list:
                article_image_path = models.ArticleImagePath(article=article, image_path=img_src)
                article_image_path.save()

            response = redirect('main:index')
            response['Location'] += f'?board={board_type}'

            return response
    else:        
        form = ArticleForm()
        board_type = request.GET.get('board', '')

    context = {
        'board_type': board_type,
        'form': form,
    }

    return render(request, 'main/article_create.html', context)
        
def get_img_src_from_html(html_text):
    img_src_list = []

    soup = BeautifulSoup(html_text, 'html.parser')
    img_tags = soup.select('img')
    for img_tag in img_tags:
        img_src_list.append(img_tag.attrs['src'])

    return img_src_list