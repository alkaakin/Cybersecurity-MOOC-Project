from django.http import HttpResponse
from .models import Entry
from django.shortcuts import render

def homePageView(request):
    fetched_entries = Entry.objects.all()
    return render(request, 'myapp/index.html', {'entries': fetched_entries})