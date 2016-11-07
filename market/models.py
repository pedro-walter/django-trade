from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(blank=True, max_length=100)
    platform = models.ForeignKey('Platform', null=True)
    platform_username = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name
        
class Platform(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
        
class Offer(models.Model):
    player = models.ForeignKey('Player')
    platform = models.ForeignKey('Platform', null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    item_offered = models.ForeignKey('Item', related_name='+')
    qty_offered = models.PositiveIntegerField("Quantity Offered", 
                                              default=1,
                                              validators=[MinValueValidator(1)])
    item_wanted = models.ForeignKey('Item', related_name='+')
    qty_wanted = models.PositiveIntegerField("Quantity Wanted", 
                                              default=1,
                                              validators=[MinValueValidator(1)])
    offerer_approved = models.BooleanField(default=False)
    bidder_approved = models.BooleanField(default=False)
    
    #Status choices
    STATUS_OFFERED      = 'OF'
    STATUS_BID_ACCEPTED = 'BA'
    STATUS_COMPLETED    = 'CO'
    STATUS_CANCELED     = 'CA'
    
    STATUS_CHOICES = (
        (STATUS_OFFERED     ,'Offered'),
        (STATUS_BID_ACCEPTED,'Bid Accepted'),
        (STATUS_COMPLETED   ,'Completed'),
        (STATUS_CANCELED    ,'Canceled'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_OFFERED,
    )           
                                          
    def __str__(self):
        return "Offer from player: {}. Offers {} {} and wants {} {}".format(
            self.player.user.username,
            self.qty_offered,
            self.item_offered.name,
            self.qty_wanted,
            self.item_wanted.name)
        
    def set_offerer_approved(self):
        self.offerer_approved = True
        self.check_completed()
        self.save()
        
    def set_bidder_approved(self):
        self.bidder_approved = True
        self.check_completed()
        self.save()  
        
    def check_completed(self):
        if self.offerer_approved and self.bidder_approved:
            self.status = self.STATUS_COMPLETED
    
class Item(models.Model):
    name = models.CharField(max_length=200)
    image_path = models.CharField(max_length=100)
    category = models.ForeignKey('ItemCategory', null=True)
    rarity = models.ForeignKey('ItemRarity', null=True)
    source = models.ForeignKey('ItemSource', null=True)
    
    def __str__(self):
        return self.name    

class ItemRarity(models.Model):
    name = models.CharField(max_length=50)
    
class ItemCategory(models.Model):
    name = models.CharField(max_length=50)
    
class ItemSource(models.Model):
    name = models.CharField(max_length=50)    

class Bid(models.Model):
    offer = models.ForeignKey('Offer')
    player = models.ForeignKey('Player')
    date_posted = models.DateTimeField(auto_now_add=True)
    accepted_for_trade = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    
    def __str__(self):
        return "Bid on offer {} from {}".format(
            self.offer.id,
            self.player.user.username)  
    
class BidMessage(models.Model):
    bid = models.ForeignKey('Bid')
    player = models.ForeignKey('Player')
    date_posted = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, max_length=10000) 
    
    def __str__(self):
        return "Message on bid {} from {}".format(
            self.bid.offer.id,
            self.player.user.username)      
    