from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    class BoardType(models.TextChoices):
        FR = 'FR', '자유게시판'
        RV = 'RV', '여행후기'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    board_type = models.CharField(max_length=2, choices=BoardType.choices, default=BoardType.FR)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

class ArticleImagePath(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image_path = models.TextField()