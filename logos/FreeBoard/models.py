from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.urls import reverse






class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('FreeBoard:index', args=[self.name])

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
    q_hit = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')
    
    def __str__(self):
        return self.subject
    
class Photo(models.Model):
    post = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    boards = models.CharField(max_length=1)
    


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    address = models.IntegerField()
    answer = models.ForeignKey(Answer, null=True, blank=True,  on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True,  on_delete=models.CASCADE)
    