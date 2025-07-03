from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Car)
admin.site.register(models.Bid)
admin.site.register(models.Auction)
admin.site.register(models.CarImage)
# The above code registers the Car, Bid, and Auction models with the Django admin site, allowing them to be managed through the admin interface.
# This is useful for managing the data related to cars, bids, and auctions in the Cars Auction application.