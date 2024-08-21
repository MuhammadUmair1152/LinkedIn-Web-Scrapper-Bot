from django.urls import path
from .views import scrape_profile

urlpatterns = [
    path('scrape/', scrape_profile, name='scrape_profile'),
]
