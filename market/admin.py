from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Player)
admin.site.register(Platform)
admin.site.register(Offer)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(BidMessage)