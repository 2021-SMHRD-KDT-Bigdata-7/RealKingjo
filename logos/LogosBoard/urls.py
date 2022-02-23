from django.urls import path
from . import views

app_name = 'Logos'

urlpatterns = [
  path('listdetail/', views.view_p, name='listdetail'),
  path('userinput/', views.input, name = 'userinput'),
  path('listcon/', views.list, name='listcon'),
  
]