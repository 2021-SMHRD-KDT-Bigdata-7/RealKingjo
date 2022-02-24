from django.shortcuts import render, get_object_or_404
from common.models import search_log

def index(request):
    
    log_list = search_log.objects.order_by('-create_date')
    log_top = log_list[0:5]
    content= {'log_top':log_top,'log_list':log_list}
    return render(request, 'MainBoard/status_form.html',content)
