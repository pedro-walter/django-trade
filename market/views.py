import requests

from django import forms
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.views.generic import TemplateView,\
                                 ListView,\
                                 View
from django.views.generic.detail import DetailView                                 
from django.views.generic.edit import CreateView,\
                                      UpdateView,\
                                      DeleteView,\
                                      FormMixin

from allauth.socialaccount.models import SocialAccount

from django_filters import FilterSet
from django_filters.views import FilterView

from email_registration.views import email_registration_confirm

from .forms import *
from .models import *

class RegistrationForm(SetPasswordForm):
    platform = forms.ModelChoiceField(queryset=Platform.objects.all())
    platform_username = forms.CharField(max_length=100)
    
    def save(self, commit=True):
        super(RegistrationForm, self).save(commit)
        Player.objects.create(user=self.user,
                              display_name=self.cleaned_data.get('platform_username'),
                              platform=self.cleaned_data.get('platform'),
                              platform_username=self.cleaned_data.get('platform_username'))
        return self.user

def email_registration(request, code, *args, **kwargs):
    return email_registration_confirm(request, code, form_class=RegistrationForm)

def steam_login(request):
    try:
        player = request.user.player
    except ObjectDoesNotExist:
        player = None
    if not player:
        social_account = SocialAccount.objects.get(
            user=request.user,
            uid__startswith='http://steamcommunity.com/openid/id/')
        steam_id = social_account.uid.split('/')[-1]
        #get data using request from steam API
        resp = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
            params = {
                'key':settings.STEAM_API_KEY,   
                'steamids':steam_id,   
            })
        steam_username = resp.json()['response']['players'][0]['personaname']   
        request.user.username = steam_username
        numeric_id_suffix = 0
        while True:
            try:
                request.user.save()
                break
            except Exception as e:
                request.user.username = steam_username + str(numeric_id_suffix)
                numeric_id_suffix += 1
        Player.objects.create(user=request.user,
                              display_name=steam_username,
                              platform=Platform.objects.get(name='Steam'),
                              platform_username=steam_username)
        
        
    return redirect('my_profile', permanent=True)
    

class PlayerList(ListView):
    model = Player
    
class PlayerDetail(DetailView):
    model = Player
    
class PlayerEditProfile(View):
    def get_context(self, request):
        return {
            'form': PlayerProfileForm(instance=request.user.player)   
        }

    def get(self, request, *args, **kwargs):
        return self.show_view(request) 
        
    def post(self, request, *args, **kwargs):
        form = PlayerProfileForm(request.POST, instance=request.user.player)
        form.save()
        return self.show_view(request)
        
    def show_view(self, request):
        return render(request, 
                      'market/player_profile.html', 
                      self.get_context(request))

class MyOffersList(ListView):
    model = Offer
    template_name = "market/offer_list_player.html"
    
    def get_context_data(self, **kwargs):
        context = super(MyOffersList, self).get_context_data(**kwargs)    
        context['my_bids'] = Bid.objects.filter(player=self.request.user.player)\
                                        .order_by('offer__status')
        return context
    
    def get_queryset(self):
        return Offer.objects.filter(player=self.request.user.player)\
                            .order_by('status')
    
class OfferListFilter(FilterSet):
    class Meta:
        model = Offer
        fields = ['platform', 'item_offered','item_wanted']    
    
class OfferList(FilterView):
    template_name = "market/offer_list_all.html"
    filterset_class = OfferListFilter
    
    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)
        kwargs['queryset'] = Offer.objects.filter(status=Offer.STATUS_OFFERED)
        return filterset_class(**kwargs)
     
     
class OfferDetail(DetailView):
    model = Offer    
    form_class = inlineformset_factory(Bid, BidMessage, 
            fields=('message','bid'),
            max_num=1,
            can_delete=False)
    
    def get_context_data(self, **kwargs):
        context = super(OfferDetail, self).get_context_data(**kwargs)
        offer = self.get_object()
        bids_data = []
        if offer.player == self.request.user.player:
            #The offer belongs to this player, show all bids and messages
            for bid in Bid.objects.filter(offer=offer):
                bids_data.append({
                    'bid':bid,
                    'form':BidMessageForm(initial={
                        'bid':bid,
                        'player':self.request.user.player,    
                    })
                })
                context['bid_action'] = 'Send message'
        else:
            
            try:
                bid = Bid.objects.get(offer=self.get_object(), 
                                      player=self.request.user.player,
                                      canceled=False)
            except Bid.DoesNotExist:
                bid = None
                   
            bid_form = None
            if bid:
                context['bid_action'] = 'Send message'
                bid_form = BidMessageForm(initial={
                    'bid':bid,
                    'player':self.request.user.player,
                })
            elif offer.status == Offer.STATUS_OFFERED:
                context['bid_action'] = 'Send bid'
                bid_form = NewBidForm(initial={
                    'player':self.request.user.player,
                })   
                
            if bid_form:    
                bids_data.append({
                    'bid':bid,
                    'form':bid_form
                })                
                
            context['bid'] = bid
            
        context['bids_data'] = bids_data
            
        return context    
        
    def post(self, *args, **kwargs):
        bid_message_form = BidMessageForm(self.request.POST)    
        if bid_message_form.is_valid():
            bid_message_form.save()
        else:
            new_bid_form = NewBidForm(self.request.POST)
            if new_bid_form.is_valid():
                new_bid_form.instance.bid = Bid.objects.create(
                    offer=self.get_object(), 
                    player=self.request.user.player)
                new_bid_form.save()
        return redirect(self.request.get_full_path(), permanent=True)

class OfferCreate(CreateView):
    model = Offer
    success_url = reverse_lazy('offer_list')
    fields = ['platform', 
              'item_offered', 
              'qty_offered', 
              'item_wanted', 
              'qty_wanted']
              
    def form_valid(self, form):
        offer = form.save(commit=False)
        offer.player = self.request.user.player
        offer.save()
        form.save()
        return super(OfferCreate, self).form_valid(form)         

class OfferUpdate(UpdateView):
    model = Offer
    success_url = reverse_lazy('my_offers_list')
    fields = ['platform', 
              'item_offered', 
              'qty_offered', 
              'item_wanted', 
              'qty_wanted']

class OfferDelete(DeleteView):
    model = Offer
    success_url = reverse_lazy('my_offers_list')
    
    def post(self, *args, **kwargs):
        offer = self.get_object()
        offer.status = Offer.STATUS_CANCELED
        offer.save()
        return redirect('my_offers_list', permanent=True)     
 
class BidDelete(DeleteView):
    model = Bid
    success_url = reverse_lazy('my_offers_list')
    
    def post(self, *args, **kwargs):
        bid = self.get_object()
        bid.canceled = True
        bid.save()           
        if bid.offer.status == Offer.STATUS_BID_ACCEPTED:
            bid.offer.status = Offer.STATUS_OFFERED
            bid.offer.save()
        return redirect('my_offers_list', permanent=True)   
 
class TradeAcceptView(DetailView):
    model = Bid    
    template_name = "market/accept_trade.html"
    
    def post(self, *args, **kwargs):
        bid = self.get_object()
        bid.offer.status = Offer.STATUS_BID_ACCEPTED
        bid.offer.save()
        bid.accepted_for_trade = True
        bid.save()
        return redirect('offer_detail', pk=bid.offer.id, permanent=True)   
 
class TradeCompleteView(DetailView):
    model = Bid    
    template_name = "market/complete_trade.html"
    
    def post(self, *args, **kwargs):
        bid = self.get_object()
        if self.request.user.player == bid.player:
            bid.offer.set_bidder_approved()
        elif self.request.user.player == bid.offer.player:
            bid.offer.set_offerer_approved()
        return redirect('offer_detail', pk=bid.offer.id, permanent=True)      