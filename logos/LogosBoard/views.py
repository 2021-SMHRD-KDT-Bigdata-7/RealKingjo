from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag



from nltk.corpus import stopwords
from numpy import append

import requests
from nltk.corpus import stopwords  

from gensim.models.word2vec import Word2Vec
from .models import TCriminal, TCriminalSummary,TLaw, Synonym
from .forms import lawform ,lawarea
from common.models import search_log 
from django.shortcuts import render
from django.utils import timezone

from django.contrib.auth import get_user_model
from konlpy.tag import Kkma
kkma = Kkma()

def Logos_Mk1 (a, b) :
  
  
    LawRating = []
    for i in range(len(b)) :   
        LawRating.append(Usado_Mk1(a,b[i]))
    
    su=max(LawRating)
    print("가장 유사한 법조문 " , b[LawRating.index(su)])


def Law_com():
    Summary= TCriminalSummary.object.all()
    Law = TLaw.objects.filter(law_type=1)
    Law['law_keyword'], Law['law_type'], Law['law_content']
    
    return Law
    



# Create your views here.


model = Word2Vec.load("static/models/classifier6")
stopword = stopwords.words('english')

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
        if word not in stopword:  
            result.append(word)  
    
    return result

def view_p(request):
    """
    pybo 내용 출력
    """
    form = lawform()
    if request.method == 'POST':
        form = lawform(request.POST)
        context = form.data['context'].replace("<br>",'\n')
        brother = form.data['brother'].replace("'","").replace('[',"").replace(']',"").split(',')
        content = form.data['content'].replace("<br>",'\n')
        subject = form.data['subject'].replace("<br>",'\n')
        keyword = form.data['keyword'].replace("<br>",'\n')
        abst = form.data['abst'].replace("<br>",'\n')
        law = form.data['law'].replace("<br>",'\n')

        #Summary = TCriminalSummary.objects.get(cri_seq=i)
        contents = {'context':context,'brother':brother,'subject':subject,'content':content,'keyword':keyword,'abst':abst,'law':law}
        
    return render(request, 'LogosBoard/logos_View.html', contents)


def input(request):
    """
    pybo 내용 출력
    """
    context = {}
    return render(request, 'LogosBoard/logos_Input.html', context)

def list(request):
    
    form = lawarea(request.POST)
    if form.is_valid():
        context = form.data['input']
        brother=Compare2(context)
        log = search_log()
        if request.user.is_authenticated :
            log.author = request.user
        else :
            log.author = get_user_model().objects.get(pk=13)
        log.content = context
        log.create_date = timezone.now()
        log.keyword = brother
        log.save()
        
        gram = []
        Summary = TCriminalSummary.objects.all()
        keytoken = kkma.nouns(context)
        for Sum in Summary:
            pojo=[]
            pojo.append(Sum)
            pojo.append(0)
            
            for token in keytoken:
                if token in Sum.cri_sum_content :
                    pojo[1] +=1
            
            gram.append(pojo)
        
        gram.sort(key=lambda x:x[1],reverse=True)
        
        sumlist = []
        for uns in gram[0:10] :
            sumlist.append(uns[0])

        content ={ "context":context,'brother':brother, "Summary":sumlist}
        
        return render(request, 'LogosBoard/logos_List.html', content)
    
    else:
        return render(request, 'LogosBoard/logos_Input.html', {'form': form})
    

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
    SYNONYM = SYNONYM.objects.all()
    synR = []
    for i in SYNONYM :
        synR.append(i.syn_content)  
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




