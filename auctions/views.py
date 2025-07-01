from django.shortcuts import render
from django.http import HttpResponse
from .models import Auction, Car, Bid
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect ,get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
            return redirect("home")
        else:
            return HttpResponse("Invalid credentials.")
    return render(request,'auctions/login.html' )

def home(request):
    return render(request, 'home.html',) 
# This view function handles requests to the auctions index page and returns a simple HTTP response.
def main_page (request):
    return render(request, 'main.html')


def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    bids = Bid.objects.filter(car=car)
    return render(request, 'car_detail.html', {'car': car, 'bids': bids})

@login_required
def place_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    car = auction.car
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
        except (TypeError, ValueError):
            messages.error(request, "Suma introdusă nu este validă.")
            return redirect('auction_detail', auction_id=auction.id)
        # Bid minim: cel mai mare bid curent sau prețul de pornire, +0.01
        existing_bids = Bid.objects.filter(car=car).order_by('-amount')
        min_bid = float(car.price)
        if existing_bids.exists():
            latest_bid = existing_bids.first()
            min_bid = float(latest_bid.amount) + 0.01 if latest_bid else float(car.price)
        if amount < min_bid:
            messages.error(request, f"Bid-ul minim este {min_bid} lei.")
            return redirect('auction_detail', auction_id=auction.id)
        Bid.objects.create(car=car, user=request.user, amount=amount)
        messages.success(request, "Bid-ul tău a fost plasat!")
        return redirect('auction_detail', auction_id=auction.id)
    return redirect('auction_detail', auction_id=auction.id)

def auction_list(request):
    auctions = Auction.objects.all()
    return render(request, 'auctions/auction_list.html', {'auctions': auctions})


def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bids = Bid.objects.filter(car=auction.car).order_by('-amount')
    return render(request, "auctions/auction_detail.html", {
        "auction": auction,
        "bids": bids,
    })

@login_required
def create_auction(request):
    cars = Car.objects.all()
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        car = Car.objects.get(id=car_id)
        auction = Auction.objects.create(
            car=car,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=7),
            is_active=True  # dacă ai câmpul acesta
        )
        return redirect('auction_list')
    return render(request, 'auctions/add_auction.html', {'cars': cars})

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

@login_required
def my_bids(request):
    bids = Bid.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'auctions/my_bids.html', {'bids': bids})