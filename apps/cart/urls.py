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
    path('search_result', search_result),
    path('cart', cart_home, name='cart'),
    path('check', check_product),
    path('order_history', order_history, name='order_history'),
    path('store_info', store_info_view, name='store_info'),
    path('new_batch', insert_batch, name='new_batch'),
    path('manage_batches', batch_management, name='manage_batches'),
    path('show_records', get_batch_product_list),
    path('set_paid', set_product_as_paid),
    path('payment_request', payment_request, name='payment_request'),
    path('finalize', set_request_as_paid),
    path('manage_supplier', create_supplier, name='manage_supplier'),
    path('set_supplier', set_user_as_supplier),
    path('manage_your_batch', show_batch, name='manage_supplier_batch'),
    path('request_payment', supplier_request, name='request_payment'),
    path('submit_request', create_request),
]
