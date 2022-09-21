# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
#from django.conf.urls import url
from apps.home import views
from apps.home.pages.profile import profileIndex
from apps.home.pages.ticket import getTicketsTable, createTicket, readTicket, closeTicket, followTicket
from helpdesk.serializers import TicketSerializer

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('index', views.index, name='index'),
    path('profile', profileIndex, name="profile"),
    path('depositFunds', views.depositFunds, name='depositFunds'),
    path('gate_about/<str:item>', views.gate_about, name='gate_about'),
    path('gate_link/<int:pk>', views.gate_link, name='gate_link'),
    path('FAQ', views.assist, name='assist'),
    #path ('send_gatelink_insertdata',views.send_gatelink_insertdata ,name = 'send_gatelink_insertdata'),
    path('area_code', views.area_code, name='area_code'),
    path('history/<str:m_str>', views.history, name='history'),
    path('Gl_Send_InsertData', views.Gl_Send_InsertData, name='Gl_Send_InsertData'),
    path('GateLink_Send_Preview_Data', views.GateLink_Send_Preview_Data,
         name='GateLink_Send_Preview_Data'),
    path('onlineSupport', views.onlineSupport, name='onlineSupport'),
    path('send_message', views.send_message, name='send_message'),
    path('get_message', views.get_message, name='get_message'),
    path('get_link_info', views.get_link_info, name='get_link_info'),
    # Get area data for Copy  button in area page
    path('get_area_all', views.get_area_all, name='get_area_all'),
    path('df_selected_ticker', views.df_selected_ticker, name='df_selected_ticker'),
    path('df_get_history', views.df_get_history, name='df_get_history'),
    path('df_deposit_click', views.df_deposit_click, name='df_deposit_click'),
    path('gl_copy_result', views.gl_copy_result, name='gl_copy_result'),

    path('history_get_info', views.history_get_info, name='history_get_info'),
    path('delete_history', views.delete_history, name='delete_history'),

    path('gateLink_get_batch_data', views.gateLink_get_batch_data,
         name='gateLink_get_batch_data'),
    path('delete_selected_batches', views.delete_selected_batches,
         name='delete_selected_batches'),
    path('download_selected_batches', views.download_selected_batches,
         name='download_selected_batches'),

    path('tickets/create', createTicket, name='tickets_create'),
    path('tickets/follow/<int:id>', followTicket, name='tickets_follow'),
    path('tickets/close/<int:id>', closeTicket, name='tickets_close'),
    path('tickets/<int:id>', readTicket, name='tickets_read'),
    path('get_tickets', getTicketsTable, name='get_tickets_table')
]
