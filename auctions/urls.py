from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_page, name='login'), 
    path('', views.home, name='home'),  # Home page of the auctions app
    path('main_page/', views.main_page, name='main_page'),  # Main page of the application
    path('auctionCars/', views.auction_list, name='cars'),  # List of active auctions
    ]