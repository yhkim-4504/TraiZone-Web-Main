from django.db import models

# Create your models here.
class Article(models.Model):
    class BoardType(models.TextChoices):
        FREE = 'FR', '자유게시판'
        REVIEW = 'RV', '여행후기'

    subject = models.CharField(max_length=200)
    board_type = models.CharField(max_length=2, choices=BoardType.choices, default=BoardType.FREE)
    content = models.TextField()
    create_date = models.DateTimeField()

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()