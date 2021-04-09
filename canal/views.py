import os
from django.conf import settings

from django.shortcuts import render
from .functions import dbc_sorter, get_asc_info, get_plots, get_plots_bitwise
from django.http import HttpResponse


def home(request):
    return render(request, 'canal/home.html')


def sorter_in(request):
    if request.method == 'GET':
        return render(request, 'canal/sorter_in.html')
    if request.method == 'POST':
        uploaded_dbc_file = request.FILES['dbcfile']
        filepath = dbc_sorter(uploaded_dbc_file)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/txt")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                return response
        return render(request, 'canal/sorter_in.html')


def can_trace_info(request):
    if request.method == 'GET':
        return render(request, 'canal/can_trace_info.html')
    if request.method == 'POST':
        uploaded_asc_file = request.FILES['ascfile']
        ch1, ch2 = get_asc_info(uploaded_asc_file)
        return render(request, 'canal/can_trace_info.html', {'ch1': ch1, 'ch2': ch2})


def can_trace_plot(request):
    if request.method == 'GET':
        return render(request, 'canal/can_trace_plot.html')
    if request.method == 'POST':
        uploaded_asc_file = request.FILES['ascfile']
        message_id = request.POST['message_id']
        scripts, divs = get_plots(uploaded_asc_file, message_id)
        context = {'scripts': scripts,
                   'divs': divs,}
        return render(request, 'canal/can_trace_plot.html', context)


def can_trace_bitwise(request):
    if request.method == 'GET':
        return render(request, 'canal/can_trace_bitwise.html')
    if request.method == 'POST':
        uploaded_asc_file = request.FILES['ascfile']
        message_id = request.POST['message_id']
        instructions = request.POST['instructions']
        # scripts, divs = get_plots_bitwise(uploaded_asc_file, message_id)
        scripts, divs, data_changes = get_plots_bitwise(uploaded_asc_file, message_id, instructions)
        context = {'scripts': scripts,
                   'divs': divs,
                   'data_changes': data_changes}
        return render(request, 'canal/can_trace_bitwise.html', context)
