# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from doctest import Example
from operator import mod
from sre_constants import SUCCESS
from timeit import default_timer
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from datetime import datetime


class site_manage(models.Model):
    st_online = "on"
    st_offline = "off"
    assin_site_status = [
        (st_online, 'Online'),
        (st_offline, 'Under Maintainance'),
    ]
    Site_Status = models.CharField(
        max_length=3,
        choices=assin_site_status,
        default=st_online,
    )
    Under_Maintainance_Message = models.CharField(
        max_length=100, help_text="Enter field Under Maintainance Message", default="")

    def __str__(self):
        return self.Site_Status


class News(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    publish_date = models.DateTimeField(default=datetime.now, blank=True)
    seen = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])


class Gate1Manage(models.Model):
    StOne = "ol"
    StTwo = "um"
    assin_Gate_status = [
        (StOne, 'online'),
        (StTwo, 'under maintenance'),
    ]
    Gate_status = models.CharField(
        max_length=2,
        choices=assin_Gate_status,
        default=StOne,
    )
    uner_mantatince_messge = models.CharField(
        max_length=100, help_text="Enter field under manitainence message")
    About_Gate = RichTextField()
    icon_about_gate = models.ImageField(max_length=100)

    def __str__(self):
        return "Gate 1 Manage"

    def get_absolute_url(self):
        return reverse('G1Manage-detail', args=[str(self.id)])


class Gate2Manage(models.Model):
    StOne = "ol"
    StTwo = "um"
    assin_Gate_status = [
        (StOne, 'online'),
        (StTwo, 'under maintenance'),
    ]
    Gate_status = models.CharField(
        max_length=2,
        choices=assin_Gate_status,
        default=StOne,
    )
    uner_mantatince_messge = models.CharField(
        max_length=100, help_text="Enter field Udermanitain Message")
    About_Gate = RichTextField()
    icon_about_gate = models.ImageField(max_length=100)

    def __str__(self):
        return "Gate 2 Manage"

    def get_absolute_url(self):
        return reverse('G2Manage-detail', args=[str(self.id)])


class Format(models.Model):
    Members_View_Format = models.CharField(max_length=100)
    Admin_Setting = models.CharField(max_length=100)
    Examples = models.TextField()

    def __str__(self):
        return self.Admin_Setting

    def get_absolute_url(self):
        return reverse('format-detail', args=[str(self.id)])


class Gate_Link(models.Model):
    GateOne = 'G1'
    GateTwo = 'G2'
    StOne = "At"
    StTwo = "Hd"
    Link_Name = models.CharField(max_length=100, help_text="Enter Link Name")
    assin_link_status = [
        (StOne, 'Active'),
        (StTwo, 'Hidden'),
    ]
    assin_link_to_gateway_choices = [
        (GateOne, 'Gate1'),
        (GateTwo, 'Gate2'),
    ]
    assin_link_to_gateway = models.CharField(
        max_length=6,
        choices=assin_link_to_gateway_choices,
        default=GateOne,
    )

    Link_price = models.FloatField(null=True)
    Link_Logo_tiny = models.ImageField(
        upload_to="images/", max_length=100, null=True)
    Link_Logo_large = models.ImageField(
        upload_to="images/", max_length=100, null=True)
    Link_Status = models.CharField(
        max_length=2,
        choices=assin_link_status,
        default=StOne,
    )

    Link_Fomart = models.ManyToManyField(
        Format, help_text="Select a Format for this Link")
    Link_Selected_Item = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.Link_Name

    def get_absolute_url(self):
        return reverse('GateLink-detail', args=[str(self.id)])


class balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    balance = models.FloatField(default=0.00, max_length=3)

    def __str__(self):
        return str(self.user)


class Message(models.Model):
    From_User = models.CharField(max_length=100, default='admin')
    To_User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    value = models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=True)
    seen = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.From_User


class TempFormat(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tmpStr = models.CharField(max_length=100)

    def __str__(self):
        return self.tmpStr


class PaymentManage(models.Model):
    Api_key = models.CharField(max_length=100)
    USDT_ADDRESS = models.TextField()
    Enable_Payment_Option_Tickets = models.CharField(max_length=200)
    Payment_Minium_orther_to_load_account = models.FloatField(
        default=0.0, help_text="USD")
    Check_for_payment_status_every = models.FloatField(
        default=0.0, help_text="min")

    def __str__(self):
        return self.Api_key


class Transaction(models.Model):
    Transaction_ID = models.CharField(max_length=100, default="")
    From_Ticket = models.CharField(max_length=100, default="")
    USDT_Reciver_Address = models.CharField(max_length=200, default="")
    Amount_Recived = models.FloatField(default=0)
    Transaction_Status = models.CharField(max_length=20, default="")
    Deposit_Received_At = models.DateTimeField(
        blank=True, default=datetime.now())
    User_Balance_updated_At = models.DateTimeField(
        blank=True, default=datetime.now())
    User_Name = models.CharField(max_length=100, default="")
    User_Balance = models.FloatField(default=0)

    def __str__(self):
        return self.Transaction_ID


class Batch(models.Model):
    batch_id = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default="Running")
    total = models.IntegerField(default=0)
    succeed = models.IntegerField(default=0)
    done = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=datetime.now(), blank=True)
    finish_time = models.DateTimeField(default=datetime.now(), blank=True)
    fail = models.IntegerField(default=0)
    remains = models.IntegerField(default=0)
    retry = models.IntegerField(default=0)
    link_name = models.CharField(max_length=100, default="#")
    user = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.batch_id)

    def get_absolute_url(self):
        return reverse('Batch-detail', args=[str(self.id)])


class Gate(models.Model):
    phone = models.CharField(max_length=100, default=0)
    DD = models.IntegerField(default=0)
    MM = models.IntegerField(default=0)
    YY = models.IntegerField(default=0)
    string1 = models.CharField(max_length=100, default="#")
    string2 = models.CharField(max_length=100, default="#")
    string3 = models.CharField(max_length=100, default="#")
    string4 = models.CharField(max_length=100, default="#")
    string5 = models.CharField(max_length=100, default="#")
    string6 = models.CharField(max_length=100, default="#")
    string7 = models.CharField(max_length=100, default="#")
    string8 = models.CharField(max_length=100, default="#")
    string9 = models.CharField(max_length=100, default="#")
    string10 = models.CharField(max_length=100, default="#")
    result1 = models.CharField(max_length=100, default="")
    result2 = models.CharField(max_length=100, default="")
    result3 = models.CharField(max_length=100, default="")
    result4 = models.CharField(max_length=100, default="")
    result5 = models.CharField(max_length=100, default="")
    batch_id = models.IntegerField(default=0)
    status = models.IntegerField(
        default=0, help_text="0:In Queue,1:Processing,2:Error,3:Done")
    gate_link_name = models.CharField(
        max_length=100, default="#", help_text="Enter field gate_link_name")
    inserted_text = models.CharField(max_length=100, default="#")
    user = models.CharField(max_length=20, default="")

    def __str__(self):
        return str(self.phone)

    def get_absolute_url(self):
        return reverse('Gate-detail', args=[str(self.id)])


class AreaCode(models.Model):
    area_code = models.CharField(max_length=10, default="000")
    areaf1 = models.CharField(max_length=100, default="#")
    areaf2 = models.CharField(max_length=100, default="#")
    areaf3 = models.CharField(max_length=100, default="#")
    areaf4 = models.CharField(max_length=100, default="#")
    areaf5 = models.CharField(max_length=100, default="#")
    areaf6 = models.CharField(max_length=100, default="#")
    areaf7 = models.CharField(max_length=100, default="#")
    areaf8 = models.CharField(max_length=100, default="#")
    areaf9 = models.CharField(max_length=100, default="#")
    areaf10 = models.CharField(max_length=100, default="#")
    

    def __str__(self):
        return self.area_code

    def get_absolute_url(self):
        return reverse('AreaCode-detail', args=[str(self.id)])


class AllowRegister(models.Model):
    st_register_on = "on"
    st_register_off = "off"
    register_status_list = [
        (st_register_on, 'Register Enabled'),
        (st_register_off, 'Register Disabled'),
    ]
    Status = models.CharField(
        max_length=3,
        choices=register_status_list,
        default=st_register_on,
    )
    Note = models.CharField(max_length=128, help_text="Enter note", default="")

    def __str__(self):
        return self.Status


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_view_time = models.DateTimeField(default=datetime.now())
    last_ticket_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.user


class FaqCategory(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class FaqContent(models.Model):
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE)
    subject = models.CharField(max_length=512)
    content = RichTextField()

    def __str__(self):
        return self.subject
