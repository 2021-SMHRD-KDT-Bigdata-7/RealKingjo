from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


from ..forms import QuestionForm
from ..models import Question, Photo, Category

@login_required(login_url='common:login')
def question_create(request, category_name):
    """
    자게 질문등록
    """
    category = get_object_or_404(Category, name=category_name)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.category = category
            question.save()
            
            for img in request.FILES.getlist('imgs'):
            # Photo 객체를 하나 생성한다.
                photo = Photo()
            # 외래키로 현재 생성한 Question의 기본키를 참조한다.
                photo.post = question
            # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                photo.image = img
            # 데이터베이스에 저장
                photo.save()
            return redirect('FreeBoard:'+str(category))
    else:
        form = QuestionForm()
    context = {'form': form, 'category': category}
    return render(request, 'FreeBoard/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    자게 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('FreeBoard:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('FreeBoard:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'category': question.category}
    return render(request, 'FreeBoard/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    자게 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('FreeBoard:detail', question_id=question.id)
    question.delete()
    return redirect('FreeBoard:index')