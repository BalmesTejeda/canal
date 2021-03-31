from django.urls import path
from . import views

app_name = 'canal'

urlpatterns = [
    path('', views.home, name='home'),
    path('sorter_in/', views.sorter_in, name='sorter_in'),
    path('can_trace_in/', views.can_trace_in, name='can_trace_in'),
    path('can_trace_chooser/', views.can_trace_chooser, name='can_trace_chooser'),
]
