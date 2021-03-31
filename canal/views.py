import os
from django.conf import settings

from django.shortcuts import render, redirect
from .functions import dbc_sorter, read_asc_file
from django.http import HttpResponse, Http404


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


def can_trace_in(request):
    print(request)
    if request.method == 'GET':
        return render(request, 'canal/can_trace_in.html')
    if request.method == 'POST':
        uploaded_asc_file = request.FILES['ascfile']
        info, data = read_asc_file(uploaded_asc_file)
        print(info)
        print(data)

        # script, div = can_plot(uploaded_asc_file)
        # return render(request, 'canal/can_trace_in.html', {'script': script, 'div': div})
        return redirect(can_trace_chooser(info, data), info=info, data=data)
        # return render(request, 'canal/can_trace_in.html')


def can_trace_chooser(info, data):
    print("Can Trace Chooser!!!")
    pass


