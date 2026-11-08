from django.urls import path

from .views import homePageView, detail

urlpatterns = [
    path('', homePageView, name='home'),
    path('entry/<int:entry_id>/', detail, name='detail'),
]