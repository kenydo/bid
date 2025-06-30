from django.shortcuts import render
from django.http import HttpResponse
from .models import Auction, Car, Bid
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect ,get_object_or_404, render
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if not username or not password or not password2:
            messages.error(request, "Toate câmpurile sunt obligatorii!")
        elif password != password2:
            messages.error(request, "Parolele nu coincid!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Acest username există deja!")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, f"Contul a fost creat cu succes pentru {username}!")
            return redirect("login") 

    return render(request, "auctions/register.html")
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login successful!")
        else:
            return HttpResponse("Invalid credentials.")
    return render(request,'auctions/login.html' )

def home(request):
    return render(request, 'home.html',) 
# This view function handles requests to the auctions index page and returns a simple HTTP response.
def main_page (request):
    return render(request, 'main.html')

def bids(request):
    auctions = Auction.objects.filter(is_active=True,end_time__gt=timezone.now()).order_by('-end_time')
    return render(request, 'auctions/bids.html')

def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    bids = Bid.objects.filter(car=car)
    return render(request, 'car_detail.html', {'car': car, 'bids': bids})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def place_bid(request, car_id):
    if request.method == 'POST':
        car = get_object_or_404(Car, id=car_id)
        amount = request.POST.get('amount')
        if amount:
            bid = Bid(car=car, user=request.user, amount=amount)
            bid.save()
            messages.success(request, "Bid placed successfully!")
            auction = Auction.objects.filter(car=car, is_active=True).first()
            if auction is not None:
                return redirect('auction_detail', auction_id=auction.id)
            else:
                return redirect('cars')
        else:
            messages.error(request, "Invalid bid amount.")
            auction = Auction.objects.filter(car=car, is_active=True).first()
            if auction is not None:
                return redirect('auction_detail', auction_id=auction.id)
            else:
                return redirect('cars')
    return HttpResponse("Method not allowed.")

def auction_detail(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    bids = Bid.objects.filter(car=auction.car)
    return render(request, 'auction_detail.html', {'auction': auction, 'bids': bids})

def create_auction(request):
    if request.method == 'POST':
        car = Car.objects.get(id=request.POST.get('car_id'))
        auction = Auction(car=car, start_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(days=7))
        auction.save()
        return HttpResponse("Auction created successfully!")
    return HttpResponse("Method not allowed.")

def create_car(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        car = Car(name=name, description=description, price=price, image=image)
        car.save()
        return redirect('main_page') 
    return render(request, 'auctions/add_car.html')