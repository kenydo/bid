from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page of the auctions app
    path('main_page/', views.main_page, name='main_page'),  # Main page of the application
]