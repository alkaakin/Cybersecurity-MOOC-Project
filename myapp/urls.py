from django.urls import include, path

from .views import detail, homePageView, add_entry

urlpatterns = [
    path('', homePageView, name='home'),
    path('entry/<int:entry_id>/', detail, name='detail'),
    path('add/', add_entry, name='add'),
    path('accounts/', include('django.contrib.auth.urls')),
]