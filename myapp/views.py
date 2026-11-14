from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
# from django.contrib.auth.signals import user_login_failed
# from django.dispatch import receiver
import logging


from .models import Entry

logger = logging.getLogger(__name__)

#FLAW 5: Security Logging and Monitoring Failures (OWASP A09:2021)
# The flaw is to not log failed login attempts, which can be exploited by attackers to brute-force passwords without being detected.
# FIX: Add a simple signal receiver to log these attempts. Uncomment the following code to fix the flaw, and also uncomment the needed imports.

# @receiver(user_login_failed)
# def log_login_failed(sender, credentials, request, **kwargs):
    # if request:
        # ip = request.META.get('REMOTE_ADDR', 'unknown IP address')
    # else:
        # ip = 'unknown IP address'
    # logger.warning(
        # "Login failed for user: %s from IP: %s",
        # credentials.get('username') or 'unknown user',
        # ip,
    # )

@login_required
def homePageView(request):
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
        return redirect('home')  

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
        # FLAW 4: Identification and Authentication Failures (OWASP A07:2021)
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if username == '' or password1 == '' or password2 == '':
            messages.error(request, "All fields are required.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        User.objects.create_user(username=username, password=password1)
        return redirect('login') 

        #FIX: Ensure that the form is valid before saving the user, replace everything from the FLAW 4 comment down to return redirect('login') with the following:
        #if form.is_valid():
            #form.save()
            #username = form.cleaned_data.get('username')
            #messages.success(request, f'Account created for {username}!')
            #return redirect('login')
    else:
        form = UserCreationForm()  
    return render(request, 'registration/register.html', {'form': form})
