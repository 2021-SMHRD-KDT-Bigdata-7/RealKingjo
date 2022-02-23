from django.shortcuts import render, get_object_or_404
from MainBoard.models import life_Question
from FreeBoard.models import Question

def index(request):

    question_list = life_Question.objects.order_by('-create_date') 
    side_question_list = Question.objects.order_by('-create_date')

    context = {'question_list': question_list[0:5],'side_question_list':side_question_list[0:5]}
    return render(request, 'MainBoard/main_from.html', context)