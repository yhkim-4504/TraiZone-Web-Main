from time import time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls.base import reverse
import main.models as models

PER_PAGE_NUM = 20

# Create your views here.
def index(request):
    board_type = request.GET.get('board', 'FR')
    page = request.GET.get('page', '1')
    
    # Get Article objects
    try:
        board_type_value = models.Article.BoardType[board_type].value
        objects = models.Article.objects.filter(board_type=board_type_value).order_by('-create_date')
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
        context = {
            'board_type': request.GET.get('board', '')
        }

        return render(request, 'main/article_create.html', context)
    else:
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        board_type = request.POST.get('board_type')

        # Check valid board_type
        try:
            board_type_value = models.Article.BoardType[board_type].value
        except:
            return HttpResponseBadRequest()

        article = models.Article(subject=subject, content=content, board_type=board_type_value, create_date=timezone.now())
        article.save()

        response = redirect('main:index')
        response['Location'] += f'?board={board_type}'

        return response