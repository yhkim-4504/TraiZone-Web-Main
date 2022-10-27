from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class ArticleAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)