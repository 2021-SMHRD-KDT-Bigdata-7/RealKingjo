from ast import keyword
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from FreeBoard.models import Category



class Search_db(models.Model):    #사전 검색테이블
    subject = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.subject
    
class life_Question(models.Model):   #생활법령 질문
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_life_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_life_question')  # 추천인 추가
    q_hit = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_life_question')
    
    
    def __str__(self):
        return self.subject



class life_Answer(models.Model):    #생활법령 답변
    
    question = models.ForeignKey(life_Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    
class Photo(models.Model):          #생활볍령 사진 넣을 모델
    post = models.ForeignKey(life_Question, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    boards = models.CharField(max_length=1)

class life_Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    address = models.IntegerField()
    life_question = models.ForeignKey(life_Question, null=True, blank=True,  on_delete=models.CASCADE)
    
    

    
    
    
    


    
    