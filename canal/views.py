import os
from django.conf import settings

from django.shortcuts import render
from .functions import dbc_sorter
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




