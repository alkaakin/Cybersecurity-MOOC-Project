from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

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

def add_entry(request):
    if request.method == 'POST':
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        owner = request.user  # Assuming the user is logged in
        new_entry = Entry(title=title, content=content, owner=owner)
        new_entry.save()
        return redirect('home') 
    else:
        return redirect('home')  # Redirect to home if not a POST request