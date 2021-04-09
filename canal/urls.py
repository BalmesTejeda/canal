from django.urls import path
from . import views

app_name = 'canal'

urlpatterns = [
    path('', views.home, name='home'),
    path('sorter_in/', views.sorter_in, name='sorter_in'),
    path('can_trace_info/', views.can_trace_info, name='can_trace_info'),
    path('can_trace_plot/', views.can_trace_plot, name='can_trace_plot'),
    path('can_trace_bitwise/', views.can_trace_bitwise, name='can_trace_bitwise'),

]
