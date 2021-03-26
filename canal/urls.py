from django.urls import path
from . import views

app_name = 'canal'

urlpatterns = [
    path('', views.home, name='home'),
    path('sorter_in/', views.sorter_in, name='sorter_in'),
    path('cantrace_in/', views.cantrace_in, name='cantrace_in'),

]