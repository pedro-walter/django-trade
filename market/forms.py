from django import forms
from django.forms import ModelForm   
                            
from .models import BidMessage, Player

class PlayerProfileForm(ModelForm):
    class Meta:
        model = Player
        fields = ['display_name', 
                  'platform', 
                  'platform_username']       
                  
bid_message_widget = forms.Textarea(attrs={
    'rows':4,       
    'cols':40,       
})                  
                  
class NewBidForm(ModelForm):
    class Meta:
        model = BidMessage
        fields = ['player', 'message']
        widgets = {
            'player':forms.HiddenInput(),   
            'message':bid_message_widget,
        }
        
class BidMessageForm(ModelForm):
    class Meta:
        model = BidMessage
        fields = ['bid','player', 'message']
        widgets = {
            'bid':forms.HiddenInput(),   
            'player':forms.HiddenInput(),   
            'message':bid_message_widget,   
        }        