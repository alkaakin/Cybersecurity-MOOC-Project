from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Entry


@login_required
def homePageView(request):
    # Intended to only show entries for the logged-in user
    fetched_entries = Entry.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'myapp/index.html', {'entries': fetched_entries})

@login_required
def detail(request, entry_id):
    try:
        # FLAW 1: Broken Access Control (OWASP A01:2021)
        # entry = Entry.objects.get(pk=entry_id)
        # FIX: Replace the above line with 
        entry = Entry.objects.get(pk=entry_id, owner=request.user)  
    except Entry.DoesNotExist:
        raise Http404("Entry does not exist")
    return render(request, 'myapp/detail.html', {'entry': entry})

@login_required
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