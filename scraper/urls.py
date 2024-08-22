from django.urls import path
from .views import scrape_user_profile

urlpatterns = [
    path('scrape/user/', scrape_user_profile, name='scrape_user_profile'),
]
