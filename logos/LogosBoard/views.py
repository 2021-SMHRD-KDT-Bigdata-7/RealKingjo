from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from konlpy.tag import Komoran
from nltk.corpus import stopwords
import re
import requests
from nltk.corpus import stopwords  

from gensim.models.word2vec import Word2Vec
from .models import TCriminal
from .models import TCriminalSummary
from .models import TLaw
from django.shortcuts import render
# 제발요


# Create your views here.


model = Word2Vec.load("static/models/classifier6")

def Compare2 (LawInput) :
    #ByeonSu=wordtoken(LawInput)
    English=kr2en(LawInput)
    Eng_list=English['translated_text']
    Eng_list=Eng_list[0][0]
    Eng_list=Eng_list.replace(",","")
    Eng_list=Eng_list.replace(".","")
    Eng_list=Eng_list.replace("[","")
    Eng_list=Eng_list.replace("]","")
    Eng_list=Eng_list.replace("'","")
    Eng_list=Eng_list.replace('"',"")
    Eng_list=Eng_list.split(" ")
    result = []
    for word in Eng_list:
        word.lower()  
        if word not in stopwords.words('english'):  
            result.append(word)  
    
    return result

def view_p(request):
    """
    pybo 내용 출력
    """
    context = {}
    return render(request, 'LogosBoard/logos_View.html', context)

def input(request):
    """
    pybo 내용 출력
    """
    context = {}
    return render(request, 'LogosBoard/logos_Input.html', context)

def list(request):
    """
    pybo 내용 출력
    """
    context = request.POST.get('input')
    Summary = TCriminalSummary.objects.filter(cri_seq = 1)
    brother=Compare2(context)

    
    content ={"context":context,'brother':brother, "Summary":Summary}
    return render(request, 'LogosBoard/logos_List.html', content)


def kr2en (Usertoken) :
    url = "https://dapi.kakao.com/v2/translation/translate"
    header = {'Authorization': 'KakaoAK 284a9924eb8117e7affebc704c4e25fc'}
    #header = {'Authorization': 'KakaoAK 3c59892324da4cd376e58acdf8bb7bc6'}
    
    data = {
        "src_lang": "kr",
        "target_lang": "en",
        "query": Usertoken
    }
    
    response = requests.get(url, headers=header, params= data)
    tokens = response.json()
    return tokens

def Compare (UserInput, LawInput) :
  
    LawInput=wordtoken(LawInput) 
    UserInput=wordtoken(UserInput)
    
    if '논논논논논' in UserInput : 
        UserInput.remove('논논논논논')
        
    ks=kr2en(LawInput)
    kc=kr2en(UserInput)

    Law_Split=list(ks.values())
    User_Split=list(kc.values())
    
    be=Law_Split[0][0][0][2:-2].split(',')
    we=User_Split[0][0][0][1:-2].split(',')

    LawEn=[]
    UserEn=[]

    for i in range(len(we)) :
        UserEn.append(we[i].strip(" ""'").lower())
        UserEn[i]=UserEn[i].split(" ")
    for i in range(len(be)) :
        LawEn.append(be[i].strip(" ""'").lower())
        LawEn[i]=LawEn[i].split(" ")
    UserT=[]
    LawT=[]
    ListD = sum(UserEn,UserT)
    ListE = sum(LawEn,LawT)
    
    print(ListD)
    print(ListE)
    return ListD, ListE


def Usado_Mk1(a, b) :
    
    a, b=Compare(a,b)
    List2 = []
    List3 = []
    
    for i in range(len(a)):
        a[i]=a[i].replace(".","")
    for i in range(len(b)):
        b[i]=b[i].replace(".","")
    
    for r in synR:
        for i in range(len(a)):
            if a[i] in r :
                List2.append(a[i])
    
    for j in synR:
        for i in range(len(b)):
            if b[i] in j :
                List3.append(b[i])

    ListA = list(set(List2))
    ListB = list(set(List3))
    ListC = []
    Sum=0
    for i in range(len(ListA)):
        if (type(ListA[i]) != str):
            ListA[i]=str(ListA[i])
    for i in range(len(ListB)):
        if (type(ListB[i]) != str):
            ListB[i]=str(ListB[i])
            
    try : 
        for i in range(len(ListA)) :
            line = [] 
            for j in range(len(ListB)) :
                line.append(model.wv.similarity(ListA[i],ListB[j]))
            ListC.append(max(line))
            Sum+=max(line)
#                 print("{a}와 {b}의 유사도 : {c}".format(a=ListA[i],b=ListB[j],c=model.wv.similarity(ListA[i],ListB[j])))

                
    except : 
        print("작동 불가!")
        
    Rating = Sum/len(ListC)
    print("유사도 평균 : {a}".format(a=Rating))
    
    if (ListB == []) :
        print("아무것도 없는데요?")
    if (ListA == []) :
        print("아무것도, 없다니까요!")
    
    return Rating


