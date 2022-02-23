from django.shortcuts import render, get_object_or_404
from MainBoard.models import Search_db
from django.core.paginator import Paginator 
from django.db.models import Q


def index(request):
    """
    pybo 목록 출력
    """
    
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    
    
     
    
    # 검색
    search_list =Search_db.objects.order_by('subject')
    if kw:
        search_list = search_list.filter(
            Q(subject__icontains=kw)  # 제목검색
            
        ).distinct()
    
    # 페이징처리
    paginator = Paginator(search_list, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'search_list': page_obj,'page': page, 'kw': kw}
    return render(request, 'MainBoard/dictionary_form.html', context)