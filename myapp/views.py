from django.http import Http404, HttpResponse
from django.shortcuts import render

from .models import Entry


def homePageView(request):
    fetched_entries = Entry.objects.all()
    return render(request, 'myapp/index.html', {'entries': fetched_entries})

def detail(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404("Entry does not exist")
    return render(request, 'myapp/detail.html', {'entry': entry})