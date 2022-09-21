# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import AllowRegister, FaqContent, News
from .models import Gate1Manage
from .models import Gate2Manage
from .models import Format
from .models import Gate_Link
from .models import balance
from .models import Message
from .models import Gate
from .models import Batch
from .models import TempFormat
from .models import AreaCode
from .models import Transaction
from .models import PaymentManage
from .models import site_manage, AllowRegister, FaqContent, FaqCategory

# Register your models here
# admin.site.register(News)
admin.site.site_header = "DataFlair Django Tutorials"


class SiteManageAdmin(admin.ModelAdmin):
    list_display = ('Site_Status', 'Under_Maintainance_Message')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'publish_date', 'seen')


class FomartAdmin(admin.ModelAdmin):
    list_display = ('id', 'Members_View_Format', 'Admin_Setting', "Examples")


class GateLinkAdmin(admin.ModelAdmin):
    list_display = ('Link_Name', 'assin_link_to_gateway', 'Link_price',
                    'Link_Logo_tiny', 'Link_Logo_large', 'Link_Status')

    def Link_Logo_tiny_preview(self, obj):
        return obj.Link_Logo_tiny_preview

    Link_Logo_tiny_preview.short_description = 'Link_Logo_tiny_preview'
    Link_Logo_tiny_preview.allow_tags = True


class MessageAdmin(admin.ModelAdmin):
    list_display = ('From_User', 'To_User', 'value', 'date', 'seen')


class GateAdmin(admin.ModelAdmin):
    list_display = ('phone', 'YY', 'MM', 'DD', 'batch_id',
                    'status', 'gate_link_name')


class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_id', 'status', 'total', 'start_time',
                    'finish_time', 'link_name', 'user')


class AreacodehAdmin(admin.ModelAdmin):
    list_display = ('area_code', 'areaf1', 'areaf2',
                    'areaf3', 'areaf4', 'areaf5', 'areaf6', 'areaf7', 'areaf8', 'areaf9', 'areaf10')


class AreacodehAdmin(admin.ModelAdmin):
    list_display = ('area_code', 'areaf1', 'areaf2',
                    'areaf3', 'areaf4', 'areaf5', 'areaf6', 'areaf7', 'areaf8', 'areaf9', 'areaf10')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('Transaction_ID', 'From_Ticket', 'USDT_Reciver_Address', 'Amount_Recived',
                    'Transaction_Status', 'Deposit_Received_At', 'User_Balance_updated_At', 'User_Name', 'User_Balance')


class PaymentManageAdmin(admin.ModelAdmin):
    list_display = ('Api_key', 'USDT_ADDRESS', 'Enable_Payment_Option_Tickets',
                    'Payment_Minium_orther_to_load_account', 'Check_for_payment_status_every')


class BalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")


class AllowRegisterAdmin(admin.ModelAdmin):
    list_display = ("Status", "Note")

class FaqContentAdmin(admin.ModelAdmin):
    list_display = ("category", "subject", "content")

# class Gate1Admin(admin.ModelAdmin):
  #  form = Gate1Form
admin.site.register(site_manage, SiteManageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Gate, GateAdmin)
admin.site.register(Gate1Manage)
admin.site.register(balance, BalanceAdmin)
admin.site.register(Gate2Manage)
admin.site.register(Format, FomartAdmin)
admin.site.register(Gate_Link, GateLinkAdmin)
admin.site.register(Message, MessageAdmin)
# admin.site.register(TempFormat)
admin.site.register(Batch, BatchAdmin)
admin.site.register(AreaCode, AreacodehAdmin)
admin.site.register(PaymentManage, PaymentManageAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(AllowRegister, AllowRegisterAdmin)

admin.site.register(FaqCategory)
admin.site.register(FaqContent, FaqContentAdmin)
