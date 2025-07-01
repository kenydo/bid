from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_page, name='login'), 
    path('', views.home, name='home'),  # Home page of the auctions app
    path('main_page/', views.main_page, name='main_page'),  # Main page of the application
    path('auction/<int:auction_id>/bid/', views.place_bid, name='place_bid'),
    path('auction/<int:auction_id>/', views.auction_detail, name='auction_detail'),  # Detail view of a specific auction
    path('auctions/', views.auction_list, name='auction_list'),  # Auctions index page
    path('add_car/', views.create_car, name='add_car'),  # Page to add a new car
    path('create_auction/', views.create_auction, name='create_auction'),    
    path('my-bids/', views.my_bids, name='bids'),
    ]