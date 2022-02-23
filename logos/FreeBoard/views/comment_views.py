from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Comment


@login_required(login_url='common:login')
def comment_create_question(request):
    """
    자게 답글댓글등록
    """
    form = CommentForm()
    context = {'form': form}
    if request.method == "POST":
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.create_date = timezone.now()
        
        if request.POST.get('category') == '1' :#자유게시판
            question = get_object_or_404(Question, pk=request.POST.get('address'))
            comment.address = request.POST.get('address')
            comment.question =  question
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('FreeBoard:detail', question_id=question.id), comment.id))
            
        elif request.POST.get('category') == '2' :#질의응답
            question = get_object_or_404(Question, pk=request.POST.get('address'))
            comment.address = request.POST.get('address')
            comment.question =  question
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('FreeBoard:detail', question_id=question.id), comment.id))
            
        elif request.POST.get('category') == '3' :#생활법률
            question = get_object_or_404(Question, pk=request.POST.get('address'))
            comment.address = request.POST.get('address')
            comment.question =  question
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('FreeBoard:detail', question_id=question.id), comment.id))
    return render(request, 'FreeBoard/get', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    자게 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('FreeBoard:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('FreeBoard:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'FreeBoard/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    자게 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('FreeBoard:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('FreeBoard:detail', question_id=comment.question.id)

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.address = request.POST.get('address')
            comment.save()
            return redirect('FreeBoard:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'FreeBoard/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    자게 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('FreeBoard:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('FreeBoard:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'FreeBoard/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    자게 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('FreeBoard:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('FreeBoard:detail', question_id=comment.answer.question.id)


