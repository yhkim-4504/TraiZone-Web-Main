from django import forms
from main.models import Article
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['subject', 'content']
        
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(),
        }

        labels = {
            'subject': '제목',
            'content': '내용',
        }  