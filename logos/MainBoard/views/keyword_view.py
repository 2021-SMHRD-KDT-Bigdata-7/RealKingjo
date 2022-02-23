from django.shortcuts import render, get_object_or_404
import urllib.request
import json
import re

def index(request):
   
    keyword = request.GET.get("word")
    if keyword=="" :
        keyword = "살인"
    headfile = naversaerch(keyword)
    keyfile = []
    for i in headfile.get('items'):
        i['title'] = re.sub('(<([^>]+)>)', '', i['title'])
        i['description'] = re.sub('(<([^>]+)>)', '', i['description'])
        keyfile.append(i)
    
    content = {"mainfile":keyfile[0],'keyfile':keyfile}
    return render(request, 'MainBoard/keyword_form.html',content)




def naversaerch (input) :
    client_id = "rVN0lQT9n6cXmjz1cY7b"
    client_secret = "UwJjNRrdxf"
    encText = urllib.parse.quote(input)
    url = "https://openapi.naver.com/v1/search/encyc.json?query=" + encText # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    
    if(rescode==200):
        response_body = response.read()
        result = json.loads(response_body)
        return result
    else:
        print("Error Code:" + rescode)