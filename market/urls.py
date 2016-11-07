"""market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from email_registration.views import email_registration_form

from .views import email_registration,\
                   steam_login,\
                   PlayerList,\
                   PlayerDetail,\
                   PlayerEditProfile,\
                   MyOffersList,\
                   OfferList,\
                   OfferDetail,\
                   OfferCreate,\
                   OfferUpdate,\
                   OfferDelete,\
                   BidDelete,\
                   TradeAcceptView,\
                   TradeCompleteView

urlpatterns = [
    url(r'^$', OfferList.as_view(), name="home"),
    url(r'^email_registration$', email_registration_form, 
                                 name='email_registration_form'),
    url(r'^email_registration/(?P<code>[^/]+)/$', email_registration, 
                                                  name='email_registration_confirm'),
    url(r'^steamlogin$', steam_login, name="steam_login"),
    url(r'^players$', PlayerList.as_view(), name="player_list"),
    url(r'^players/(?P<pk>\d+)$', PlayerDetail.as_view(), name="player_detail"),
    url(r'^myoffers$', MyOffersList.as_view(), name="my_offers_list"),
    url(r'^myprofile$', PlayerEditProfile.as_view(), name="my_profile"),
    url(r'^offers$', OfferList.as_view(), name="offer_list"),
    url(r'^offers/(?P<pk>\d+)$', OfferDetail.as_view(), name="offer_detail"),
    url(r'^offers/new$', OfferCreate.as_view(), name="offer_new"),
    url(r'^offers/edit/(?P<pk>\d+)$', OfferUpdate.as_view(), name="offer_edit"),
    url(r'^offers/delete/(?P<pk>\d+)$', OfferDelete.as_view(), name="offer_delete"),
    url(r'^bid/delete/(?P<pk>\d+)$', BidDelete.as_view(), name="bid_delete"),
    url(r'^accept_trade/(?P<pk>\d+)$', TradeAcceptView.as_view(), name="accept_trade"),
    url(r'^complete_trade/(?P<pk>\d+)$', TradeCompleteView.as_view(), name="complete_trade"),
]
