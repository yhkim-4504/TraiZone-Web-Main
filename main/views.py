from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
import main.models as models

# Create your views here.
def index(request):
    board_type = request.GET.get('board', 'free')
    page = request.GET.get('page', '1')
    
    # Get Article objects
    if board_type == 'free':
        objects = models.Article.objects.filter(board_type='FR').order_by('-create_date')
        board_name = models.Article.BoardType.FREE.label
    elif board_type == 'review':
        objects = models.Article.objects.filter(board_type='RV').order_by('-create_date')
        board_name = models.Article.BoardType.REVIEW.label
    else:
        objects = None
        board_name = '존재하지 않는 게시판입니다.'

    objects = Paginator(objects, 20).get_page(page)

    context = {'article_list': objects, 'board_name': board_name, 'board_type': board_type}

    return render(request, 'main/index.html', context)

def detail(request, article_id):
    return HttpResponse('detail')