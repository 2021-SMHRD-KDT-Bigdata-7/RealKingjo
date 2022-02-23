from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Photo, Question, Category

def index(request, category_name='free'):
    """
    자게 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    
    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)
    
    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date') & Question.objects.filter(category=category)
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')  & Question.objects.filter(category=category)
    else:  # recent
        question_list = Question.objects.order_by('-create_date')  & Question.objects.filter(category=category)

    # 검색
    
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
    
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'category_list': category_list, 'category': category}
    return render(request, 'FreeBoard/question_list.html', context)

def qnalist(request, category_name='qna'):
    """
    질문 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    
    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)
    
    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')  & Question.objects.filter(category=category)
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')  & Question.objects.filter(category=category)
    else:  # recent
        question_list = Question.objects.order_by('-create_date')  & Question.objects.filter(category=category)

    # 검색
    
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
    
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'category_list': category_list, 'category': category}
    return render(request, 'FreeBoard/question_list.html', context)

def detail(request, question_id):
    """
    자게 내용 출력
    """
    
    question = get_object_or_404(Question, pk=question_id)
    photo = Photo.objects.filter(post=question_id,boards='1')
    cnt = Question.objects.get(pk=question_id)
    cnt.q_hit +=1
    cnt.save()
    context = {'question': question,'photos': photo}
#    return render(request, 'FreeBoard/question_detail.html', context)
    return render(request, 'FreeBoard/single_post.html', context)
