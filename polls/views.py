from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return render(request, 'home.html',) 
# This view function handles requests to the polls index page and returns a simple HTTP response.
def main_page (request):
    return render(request, 'main.html')
