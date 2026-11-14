from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import redirect, render

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
        entry = Entry.objects.get(pk=entry_id)
        # FIX: Replace the above line with 
        # entry = Entry.objects.get(pk=entry_id, owner=request.user)  
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

@login_required
def search(request):
    query = request.GET.get('q', '')
    if query:
        # FLAW 3: SQL Injection (OWASP A03:2021)
        results = Entry.objects.raw(f"SELECT * FROM myapp_entry WHERE owner_id = {request.user.id} AND title LIKE '%%{query}%%' ORDER BY created_at DESC")
        # FIX: Use Django's ORM filtering instead of raw SQL to prevent SQL injection, replace with below line
        # results = Entry.objects.filter(owner=request.user, title__icontains=query).order_by('-created_at')
    else:
        results = []
    return render(request, 'myapp/search_results.html', {'results': results, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})