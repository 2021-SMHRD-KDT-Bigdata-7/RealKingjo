
from django.urls import path
from .views import main_views
from .views import lifepost_views
from .views import join_view
from .views import mypage_view
from .views import dictionary_view
from .views import status_view
from .views import keyword_view


app_name = 'MainBoard'


urlpatterns = [
    path('', main_views.index,name='main'),
    path('lifepost', lifepost_views.index,name='lifepost'),
    path('join', join_view.index,name='join'),
    path('mypage', mypage_view.index,name='mypage'),
    path('mypage/update', mypage_view.update,name='update'),
    path('dictionary', dictionary_view.index,name='dictionary'),
    path('status', status_view.index,name='status'),
    path('keyword', keyword_view.index,name='keyword'),
    path('keyword/<word>', keyword_view.detail,name='keywordselect'),
    path('<int:life_question_id>/', lifepost_views.detail,name='lifedetail'),
    
    path('question/create/', lifepost_views.question_create, name='life_question_create'),
    path('question/modify/<int:life_question_id>/', lifepost_views.question_modify, name='life_question_modify'),
    path('question/delete/<int:life_question_id>/', lifepost_views.question_delete, name='life_question_delete'),
    path('question/craete/<int:category_id>/', lifepost_views.question_create, name='life_question_create'),
    path('question/list/life', lifepost_views.index, name='life'),
    
    
    path('comment/create/question/', lifepost_views.comment_create_question, name='life_comment_create_question'),
    path('comment/modify/question/<int:life_comment_id>/', lifepost_views.comment_modify_question, name='life_comment_modify_question'),
    path('comment/delete/question/<int:life_comment_id>/', lifepost_views.comment_delete_question, name='life_comment_delete_question'),
]