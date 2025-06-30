from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_page, name='login'), 
    path('', views.home, name='home'),  # Home page of the auctions app
    path('main_page/', views.main_page, name='main_page'),  # Main page of the application
    path('bids/', views.bids, name='bids'),  # List of active auctions
    path('auction/<int:auction_id>/', views.auction_detail, name='auction_detail'),  # Detail view of a specific auction
    path('add_car/', views.create_car, name='add_car'),  # Page to add a new car
    ]