from time import time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls.base import reverse
from .forms import ArticleForm
import main.models as models

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
    comment_list = article.comment_set.all()

    context = {
        'article': article,
        'comment_list': comment_list, 
    }

    return render(request, 'main/detail.html', context)

def comment_create(request, article_id):
    content = request.POST.get('content', '')
    article = get_object_or_404(models.Article, id=article_id)

    comment = models.Comment(article=article, content=content, create_date=timezone.now())
    comment.save()

    return redirect('main:detail', article_id=article_id)

def article_create(request):
    if request.method == 'GET':
        form = ArticleForm()
        context = {
            'board_type': request.GET.get('board', ''),
            'form': form,
        }

        return render(request, 'main/article_create.html', context)
    else:
        board_type = request.POST.get('board_type', 'FR')
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.create_date = timezone.now()
            article.save()

            response = redirect('main:index')
            response['Location'] += f'?board={board_type}'

            return response
        
        else:
            return HttpResponseBadRequest()
        