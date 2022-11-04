from django import forms
from . import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['subject', 'content', 'board_type']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '700px'}}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
            'board_type': '게시판분류',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']
        labels = {
            'content': '내용'
        }