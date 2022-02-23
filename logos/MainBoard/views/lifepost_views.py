from django.shortcuts import render, get_object_or_404,redirect, resolve_url
from django.utils import timezone
from MainBoard.models import life_Question,life_Answer,Photo, life_Comment
from ..forms import life_QuestionForm,CommentForm
from django.core.paginator import Paginator 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count
from FreeBoard.models import Category, Question

def index(request, category_name='life'):
    """
    생활법률 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    
    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = life_Question.objects.order_by('-create_date')  & life_Question.objects.filter(category=category)
        
    # 인가
    top_question_list = life_Question.objects.annotate(num_voter=Count('q_hit')).order_by('-create_date') & life_Question.objects.filter(category=category)
    side_question_list = Question.objects.order_by('-create_date')
    


    # 검색
    
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw)  # 질문 글쓴이검색
            
        ).distinct()
    
    # 페이징처리
    paginator = Paginator(question_list, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)

    
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'category_list': category_list, 'category': category, 'top_paginator':top_question_list[0:3],'side_question_list':side_question_list[0:5]}
    return render(request, 'MainBoard/lifepost_list.html', context)
 

def detail(request, life_question_id):
    """
    생활법률 내용 출력
    """
    
    question = get_object_or_404(life_Question, pk=life_question_id)
    side_question_list = life_Question.objects.order_by('-create_date')
    photo = Photo.objects.filter(post=life_question_id,boards='1')
    cnt = life_Question.objects.get(pk=life_question_id)
    cnt.q_hit +=1
    cnt.save()
    context = {'question': question,'photos': photo ,'side_question_list':side_question_list[0:5]}
#    return render(request, 'FreeBoard/question_detail.html', context)
    return render(request, 'MainBoard/lifepost_detail.html', context)


@login_required(login_url='common:login')
def question_create(request, category_id):
    """
    생활 글쓰기
    """
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = life_QuestionForm(request.POST)
        if form.is_valid():
            life_question = form.save(commit=False)
            life_question.author = request.user  # author 속성에 로그인 계정 저장
            life_question.create_date = timezone.now()
            life_question.category = category
            life_question.save()
            
            for img in request.FILES.getlist('imgs'):
            # Photo 객체를 하나 생성한다.
                photo = Photo()
            # 외래키로 현재 생성한 Question의 기본키를 참조한다.
                photo.post = life_question
            # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                photo.image = img
            # 데이터베이스에 저장
                photo.save()
            return redirect('MainBoard:'+str(category))
    else:
        form = life_QuestionForm()
    context = {'form': form, 'category': category}
    return render(request, 'MainBoard/lifepost_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, life_question_id):
    """
    글쓰기 질문수정
    """
    life_question = get_object_or_404(life_Question, pk=life_question_id)
    if request.user != life_question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('MainBoard:lifedetail', question_id=life_question.id)

    if request.method == "POST":
        form = life_QuestionForm(request.POST, instance=life_question)
        if form.is_valid():
            life_question = form.save(commit=False)
            life_question.modify_date = timezone.now()  # 수정일시 저장
            life_question.save()
            
            return redirect('MainBoard:lifedetail', question_id=life_question.id)
    else:
        form = life_QuestionForm(instance=life_question)
    context = {'form': form, 'category': life_question.category}
    return render(request, 'MainBoard/lifepost_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, life_question_id):
    """
    글쓰기 삭제
    """
    life_question = get_object_or_404(life_Question, pk=life_question_id)
    if request.user != life_question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('MainBoard:lifedetail', life_question_id=life_question.id)
    life_question.delete()
    return redirect('MainBoard:lifepost')


@login_required(login_url='common:login')
def comment_create_question(request):
    """
    pybo 질문댓글등록
    """
    form = CommentForm()
    context = {'form': form}
    if request.method == "POST":
        form = CommentForm(request.POST)
        life_comment = form.save(commit=False)
        life_comment.author = request.user
        life_comment.create_date = timezone.now()
        question = get_object_or_404(life_Question, pk=request.POST.get('address'))
        life_comment.address = request.POST.get('address')
        life_comment.life_question =  question
        life_comment.save()
        return redirect('{}#comment_{}'.format(
            resolve_url('MainBoard:lifedetail', life_question_id=question.id), life_comment.id))
        
    return render(request, 'MainBoard/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, life_comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(life_Comment, pk=life_comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('MainBoard:lifedetail', question_id=comment.life_question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('MainBoard:lifedetail', life_question_id=comment.life_question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'MainBoard/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, life_comment_id):
    """
    pybo 질문댓글삭제
    """
    comment = get_object_or_404(life_Comment, pk=life_comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('MainBoard:lifedetail', life_question_id=comment.life_question.id)
    else:
        comment.delete()
    return redirect('MainBoard:lifedetail', life_question_id=comment.life_question.id)
