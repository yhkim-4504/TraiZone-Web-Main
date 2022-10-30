from django import forms
from main.models import Article
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['subject', 'content', 'board_type']
        
        widgets = {
            'content': SummernoteWidget(),
        }