# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
#from django.conf.urls import url
from .views import *

urlpatterns = [
    # The home page
    path('search', search, name='search'),
    path('search_result', search_result, name='search_result'),
    path('cart', cart_home, name='cart'),
    path('check', check_product, name='check'),
    path('order_history', order_history, name='order_history'),
    path('store_info', store_info_view, name='store_info'),
    path('new_batch', insert_batch, name='new_batch'),
    path('manage_batches', batch_management, name='manage_batches'),
]
