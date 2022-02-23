from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from FreeBoard.models import Question, Answer, Comment
from django.conf import settings
User = settings.AUTH_USER_MODEL

def index(request):
    User=request.user
    question_list = Question.objects.filter( author = User.id )
    answer_list = Answer.objects.filter( author = User.id )
    comment_list = Comment.objects.filter( author = User.id )
    my_question_list = {'question_list': question_list , 'comment_list' : comment_list, 'answer_list' : answer_list}
    return render(request, 'MainBoard/mypage_from.html',my_question_list)


