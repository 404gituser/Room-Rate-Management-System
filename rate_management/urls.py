from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.room_rates, name= 'home'),
    path('add_rate/', view=views.add_rate, name= 'add_rate'),
    path('edit_rate/<int:pk>', view=views.edit_rate, name= 'edit_rate'),
    path('delete_rate/<int:pk>', view=views.delete_rate, name= 'delete_rate'),
    # path('rate_details', view=views.rate_details, name= 'rate_details'),
    path('rate_details/<int:pk>', view=views.rate_details, name= 'rate_details'),
    path('add_override/', view=views.add_overriden_rate, name= 'add_override'),
    path('edit_override/<int:pk>', view=views.edit_overriden_rate, name= 'edit_override'),
    path('delete_override/<int:pk>', view=views.delete_overriden_rate, name= 'delete_override'),
    path('discounts/', view=views.discounts, name= 'discounts'),
    path('add_discount/', view=views.add_discount, name= 'add_discount'),
    path('edit_discount/<int:pk>', view=views.edit_discount, name= 'edit_discount'),
    path('delete_discount/<int:pk>', view=views.delete_discount, name= 'delete_discount'),
    path('rate_offers/', view=views.rate_offers, name= 'rate_offers'),


]
