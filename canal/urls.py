from django.urls import path
from . import views

app_name = 'canal'

urlpatterns = [
    path('', views.home, name='home'),
    path('sorter_in/', views.sorter_in, name='sorter_in'),

]