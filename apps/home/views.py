# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from dataclasses import dataclass
from math import fabs
from django. contrib. auth. models import User
from datetime import datetime
from . import cnio_api
import random
from posixpath import split
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from .models import News, AccessLog
from .models import Gate1Manage
from .models import Gate2Manage
from .models import Gate_Link
from .models import balance
from .models import Message
from .models import TempFormat
from .models import Gate
from .models import Batch
from .models import AreaCode
from .models import PaymentManage
from .models import Transaction
from .models import site_manage, FaqCategory, FaqContent
from django.db.models import Q
import json
import re
import pprint

from helpdesk.models import Ticket, FollowUp

from .forms import AreaCodeForm
from .pages.ticket import CreateTicketForm
from apps.cart.models import Cart


def get_default_page_context(request):
    last_login_time = datetime.min
    last_ticket_time = datetime.min
    access_logs = AccessLog.objects.filter(user=request.user).all()
    if len(access_logs) > 0:
        item = AccessLog.objects.get(user=request.user)
        last_login_time = item.last_view_time
        last_ticket_time = item.last_ticket_time

    serverUM = False
    serverMsg = ""

    sm = site_manage.objects.all()
    if len(sm) > 0 and sm[0].Site_Status == "off":
        serverUM = True
        serverMsg = sm[0].Under_Maintainance_Message

    user = balance.objects.get(user=request.user)

    # ? Modified by Andrew (for shoping cart)
    cart_obj = Cart.objects.new_or_get(request)
    count_product = cart_obj.products.count()


    liveGateLinks = None
    gm1 = Gate1Manage.objects.all()
    if len(gm1) == 0 or gm1[0].Gate_status == "ol":
        liveGateLinks = Gate_Link.objects.filter(
            assin_link_to_gateway="G1").filter(Link_Status="At")
    gm2 = Gate2Manage.objects.all()
    if len(gm2) == 0 or gm2[0].Gate_status == "ol":
        if liveGateLinks != None:
            liveGateLinks |= Gate_Link.objects.filter(
                assin_link_to_gateway="G2").filter(Link_Status="At")
        else:
            liveGateLinks = Gate_Link.objects.filter(
                assin_link_to_gateway="G2").filter(Link_Status="At")

    context = {
        "serverUM": serverUM,
        "serverMsg": serverMsg,
        "balance": user.balance,
        # ? Modified by Andrew (for shoping cart)
        "count_product": count_product,

        "Admin_Status": 1,
        "gateLink": liveGateLinks,
        "Gate1_About_Image": {"url": "/static/assets/images/gate/gate1_about.png"},
        "Gate2_About_Image": {"url": "/static/assets/images/gate/gate2_about.png"},
        "Gate_Links": liveGateLinks,
        "unseen_news_count": len(News.objects.filter(publish_date__range=[last_login_time, datetime.max])),
        "unseen_messages_count": len(FollowUp.objects.filter(Q(user=request.user)).filter(date__range=[last_ticket_time, datetime.max])) +
        len(Ticket.objects.filter(Q(assigned_to=request.user) | Q(
            assigned_to=None)).filter(modified__range=[last_ticket_time, datetime.max]))
    }
    sm = site_manage.objects.all()
    if len(sm) > 0 and sm[0].Site_Status == "off":
        context["Admin_Status"] = 0
    gm1 = Gate1Manage.objects.all()
    if len(gm1) > 0:
        context["Gate1_About_Image"] = gm1[0].icon_about_gate
    gm2 = Gate2Manage.objects.all()
    if len(gm2) > 0:
        context["Gate1_About_Image"] = gm2[0].icon_about_gate

    return context


def mid(str, index, count):
    tmp_str = ""
    for i in range(index, index+count):
        tmp_str += str[i]
    return tmp_str


def check_BatchID():
    batchs = Batch.objects.order_by("-batch_id").all()
    if len(batchs) == 0:
        return 1
    return int(batchs[0].batch_id) + 2


def check_format(format, data, format_user):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("__________Check_format_______________")
    tmp_check_dic = {}
    tmp_check_dic['error'] = ""
    pp.pprint(format)
    pp.pprint(data)
    pp.pprint(format_user)
    tmp_format = "#".join(format)
    pp.pprint(tmp_format)
    if len(format) != len(data):
        if len(format) > len(data):
            for i in range(len(format)):
                if i >= len(data):
                    tmp_check_dic[str(format[i])] = ""
                else:
                    tmp_check_dic[str(format[i])] = data[i]
                tmp_check_dic['error'] = "Missing Data\r\n"
        else:
            for i in range(len(format)):
                tmp_check_dic[str(format[i])] = data[i]
            # tmp_check_dic['error']="count error\r\n"
    else:
        pp.pprint("__________Check_format11_______________")
        for i in range(len(format)):
            tmp_check_dic[str(format[i])] = data[i]

    pp.pprint(tmp_check_dic)
    if tmp_check_dic.get("YYYY") != None:
        if len(tmp_check_dic.get("YYYY")) < 4:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["YY"] = str(tmp_check_dic.get("YYYY"))[2:]
        tmp_format = tmp_format.replace("YYYY", "YY")
        tmp_check_dic.pop("YYYY")
    if tmp_check_dic.get("YYMMDD") != None:
        if len(tmp_check_dic.get("YYMMDD")) < 6:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["YY"] = str(tmp_check_dic.get("YYMMDD"))[:2]
        tmp_check_dic["MM"] = str(tmp_check_dic.get("YYMMDD"))[2:4]
        tmp_check_dic["DD"] = str(tmp_check_dic.get("YYMMDD"))[4:6]
        tmp_format = tmp_format.replace("YYMMDD", "YY#MM#DD")
        tmp_check_dic.pop("YYMMDD")
    if tmp_check_dic.get("YYDDMM") != None:
        if len(tmp_check_dic.get("YYDDMM")) < 6:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["YY"] = str(tmp_check_dic.get("YYDDMM"))[:2]
        tmp_check_dic["DD"] = str(tmp_check_dic.get("YYDDMM"))[2:4]
        tmp_check_dic["MM"] = str(tmp_check_dic.get("YYDDMM"))[4:6]
        tmp_format = tmp_format.replace("YYDDMM", "YY#DD#MM")
        tmp_check_dic.pop("YYDDMM")
    if tmp_check_dic.get("MMDDYY") != None:
        if len(tmp_check_dic.get("MMDDYY")) < 6:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["MM"] = str(tmp_check_dic.get("MMDDYY"))[:2]
        tmp_check_dic["DD"] = str(tmp_check_dic.get("MMDDYY"))[2:4]
        tmp_check_dic["YY"] = str(tmp_check_dic.get("MMDDYY"))[4:6]
        tmp_format = tmp_format.replace("MMDDYY", "MM#DD#YY")
        tmp_check_dic.pop("MMDDYY")
    if tmp_check_dic.get("MMYYDD") != None:
        if len(tmp_check_dic.get("MMYYDD")) < 6:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["MM"] = str(tmp_check_dic.get("MMYYDD"))[:2]
        tmp_check_dic["YY"] = str(tmp_check_dic.get("MMYYDD"))[2:4]
        tmp_check_dic["DD"] = str(tmp_check_dic.get("MMYYDD"))[4:6]
        tmp_format = tmp_format.replace("MMYYDD", "MM#YY#DD")
        tmp_check_dic.pop("MMYYDD")
    if tmp_check_dic.get("DDYYMM") != None:
        if len(tmp_check_dic.get("DDYYMM")) < 6:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["DD"] = str(tmp_check_dic.get("DDYYMM"))[:2]
        tmp_check_dic["YY"] = str(tmp_check_dic.get("DDYYMM"))[2:4]
        tmp_check_dic["MM"] = str(tmp_check_dic.get("DDYYMM"))[4:6]
        tmp_format = tmp_format.replace("DDYYMM", "DD#YY#MM")
        tmp_check_dic.pop("DDYYMM")
    if tmp_check_dic.get("DDMMYY") != None:
        if len(tmp_check_dic.get("DDMMYY")) < 6:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["DD"] = str(tmp_check_dic.get("DDMMYY"))[:2]
        tmp_check_dic["MM"] = str(tmp_check_dic.get("DDMMYY"))[2:4]
        tmp_check_dic["YY"] = str(tmp_check_dic.get("DDMMYY"))[4:6]
        tmp_format = tmp_format.replace("DDMMYY", "DD#MM#YY")
        tmp_check_dic.pop("DDMMYY")
    if tmp_check_dic.get("DDMM") != None:
        if len(tmp_check_dic.get("DDMM")) < 4:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["DD"] = str(tmp_check_dic.get("DDMMYY"))[:2]
        tmp_check_dic["MM"] = str(tmp_check_dic.get("DDMMYY"))[2:4]
        tmp_check_dic["YY"] = str(tmp_check_dic.get("DDMMYY"))[4:6]
        tmp_format = tmp_format.replace("DDMM", "DD#MM")
        tmp_check_dic.pop("DDMMYY")
    if tmp_check_dic.get("DDYY") != None:
        if len(tmp_check_dic.get("DDYY")) < 4:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["DD"] = str(tmp_check_dic.get("DDMYY"))[:2]
        tmp_check_dic["YY"] = str(tmp_check_dic.get("DDMYY"))[2:4]
        tmp_format = tmp_format.replace("DDYY", "DD#YY")
        tmp_check_dic.pop("DDYY")
    if tmp_check_dic.get("MMYY") != None:
        if len(tmp_check_dic.get("MMYY")) < 4:
            tmp_check_dic['error'] = "wrong EXP. Date\r\n"
        tmp_check_dic["MM"] = str(tmp_check_dic.get("MMYY"))[:2]
        tmp_check_dic["YY"] = str(tmp_check_dic.get("MMYY"))[2:4]
        tmp_format = tmp_format.replace("MMYY", "MM#YY")
        tmp_check_dic.pop("MMYY")
    if tmp_check_dic.get("MMDD") != None:
        if len(tmp_check_dic.get("MMDD")) < 4:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["MM"] = str(tmp_check_dic.get("MMDD"))[:2]
        tmp_check_dic["DD"] = str(tmp_check_dic.get("MMDD"))[2:4]
        tmp_format = tmp_format.replace("MMDD", "MM#DD")
        tmp_check_dic.pop("MMDD")
    if tmp_check_dic.get("YYDD") != None:
        if len(tmp_check_dic.get("YYDD")) < 4:
            tmp_check_dic['error'] = "Missing Data\r\n"
        tmp_check_dic["YY"] = str(tmp_check_dic.get("YYDD"))[:2]
        tmp_check_dic["DD"] = str(tmp_check_dic.get("YYDD"))[2:4]
        tmp_format = tmp_format.replace("YYDD", "YY#DD")
        tmp_check_dic.pop("YYDD")
    if tmp_check_dic.get("YYMM") != None:
        if len(tmp_check_dic.get("YYMM")) < 4:
            tmp_check_dic['error'] = "wrong EXP. Date\r\n"
        tmp_check_dic["YY"] = str(tmp_check_dic.get("YYMM"))[:2]
        tmp_check_dic["MM"] = str(tmp_check_dic.get("YYMM"))[2:4]
        tmp_format = tmp_format.replace("YYMM", "YY#MM")
        tmp_check_dic.pop("YYMM")

    TempFormat.objects.filter(user=format_user).delete()
    new_TmpFormat = TempFormat.objects.create(
        user=format_user, tmpStr=tmp_format)
    new_TmpFormat.save()

    if tmp_check_dic.get("DD") != None and tmp_check_dic.get("DD") != "":
        if tmp_check_dic['DD'].isdigit() == True:
            if int(tmp_check_dic['DD']) == 0 or int(tmp_check_dic['DD']) > 31:
                tmp_check_dic['error'] += tmp_check_dic['DD'] + \
                    ":is not valid Day value\r\n"
            if tmp_check_dic.get('MM') != None:
                if tmp_check_dic['MM'].isdigit() == True:
                    if int(tmp_check_dic['MM']) == 2 and int(tmp_check_dic['DD']) > 28:
                        tmp_check_dic['error'] += tmp_check_dic['DD'] + \
                            ":is not valid Day value\r\n"
        else:
            tmp_check_dic['error'] += tmp_check_dic['DD'] + \
                ":is not number\r\n"
    if tmp_check_dic.get("MM") != None and tmp_check_dic.get("MM") != "":
        if tmp_check_dic['MM'].isdigit() == True:
            if int(tmp_check_dic['MM']) == 0 or int(tmp_check_dic['MM']) > 12:
                tmp_check_dic['error'] += tmp_check_dic['MM'] + \
                    ":is not valid Month value\r\n"
        else:
            tmp_check_dic['error'] += tmp_check_dic['MM'] + \
                ":is not number\r\n"
    if tmp_check_dic.get("YY") != None and tmp_check_dic.get("YY") != "":
        if tmp_check_dic['YY'].isdigit() == False:
            tmp_check_dic['error'] += tmp_check_dic['YY'] + \
                ":is not number\r\n"
        elif len(tmp_check_dic['YY']) > 2:
            tmp_check_dic['error'] += tmp_check_dic['YY'] + \
                ":is not valid Year value\r\n"
        if int(tmp_check_dic['YY']) < datetime.now().year % 100:

            tmp_check_dic['error'] += tmp_check_dic['YY'] + \
                ":is not valid Year value11\r\n"

    pp.pprint("__________Check_format12_______________")
    pp.pprint(tmp_check_dic)
    return tmp_check_dic


def convert_format(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("Test(convert_format)-------input data----------")
    pp.pprint(data)
    # if len(data) <5:  # Check to empty string
    #    return ""

    pb_format_array = re.split('[^a-zA-Z0-9()+-]', data)

    pp.pprint("Test(convert_format)-------split data----------")
    pp.pprint(pb_format_array)

    x = ""
    cnt = 0
    for kk in pb_format_array:
        if kk != '':
            cnt += 1
            if cnt == 1:
                x = kk
            else:
                x += "#"+kk
    # x = "#".join(pb_format_array)
    pp.pprint("Test(convert_format)-------out data----------")
    pp.pprint(x)

    return x


@login_required(login_url="/login/")
def index(request):
    access_logs = AccessLog.objects.filter(user=request.user).all()
    if len(access_logs) > 0:
        item = AccessLog.objects.get(user=request.user)
        item.last_view_time = datetime.utcnow()
        item.save()
    else:
        item = AccessLog.objects.create(user=request.user)
        item.save()

    pp = pprint.PrettyPrinter(indent=4)

    news = News.objects.order_by('-publish_date').all()
    if balance.objects.filter(user=request.user).exists():
        user = balance.objects.get(user=request.user)
    else:
        new_balance = balance.objects.create(user=request.user, balance=0)
        new_balance.save()
        user = balance.objects.get(user=request.user)
    context = {
        'news': news,
        'balance': user.balance
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


@login_required(login_url="/login/")
def depositFunds(request):
    pp = pprint.PrettyPrinter(indent=4)
    GateLink = Gate_Link.objects.all()
    cnio = cnio_api.cnio()
    pm = PaymentManage.objects.all()
    apiKey = ""
    m_strTicker = ""
    for m_item in pm:
        m_strTicker = m_item.Enable_Payment_Option_Tickets
        apiKey = m_item.Api_key
        min_amount = m_item.Payment_Minium_orther_to_load_account
    m_arrayTicker = m_strTicker.split(';')
    pp.pprint(m_arrayTicker)
    cnio.api_key(apiKey)

    tmp_arrayTicker = []
    # for m_tItem in d:
    for tmp_inTicker in m_arrayTicker:
        pp.pprint(str(tmp_inTicker).lower())
        res = cnio.currenciesInfo(str(tmp_inTicker).lower())
        pp.pprint(res)
        new_res = res.decode('utf-8')
        d = json.loads(new_res)
        tmp_dicTiker = {
            'ticker': str(d['ticker']),
            'img': d['image'],
            'name': d['name'],
        }
        tmp_arrayTicker.append(tmp_dicTiker)

    pp.pprint(tmp_arrayTicker)
    user = balance.objects.get(user=request.user)
    context = {
        'segmment': 'depositFunds',
        'gateLink': GateLink,
        'balance': user.balance,
        'tickers': tmp_arrayTicker,
        'min_amount': min_amount
    }
    html_template = loader.get_template('home/depositFunds.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


@login_required(login_url="/login/")
def assist(request):
    context = {
        "categories": FaqCategory.objects.all(),
        "contents": FaqContent.objects.all()
    }

    html_template = loader.get_template('home/faq.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


@login_required(login_url="/login/")
def gate_about(request, item):
    underMaintainance = False
    status = None

    user = balance.objects.get(user=request.user)
    pp = pprint.PrettyPrinter(indent=4)

    if item == 'G1':
        m_pk = 1
        about = Gate1Manage.objects.filter(Gate_status="ol")
        if len(Gate1Manage.objects.filter(Gate_status="um")) > 0:
            underMaintainance = True
            status = Gate1Manage.objects.filter(Gate_status="um")[0]

    elif item == 'G2':
        m_pk = 2
        about = Gate2Manage.objects.filter(Gate_status="ol")
        if len(Gate2Manage.objects.filter(Gate_status="um")) > 0:
            underMaintainance = True
            status = Gate2Manage.objects.filter(Gate_status="um")[0]
    else:
        redirect("/index")

    gate = Gate.objects.all()
    batch = Batch.objects.all()
    if item == 'G1':
        ness_GateLink = Gate_Link.objects.filter(
            assin_link_to_gateway='G1').filter(Link_Status="At")
    elif item == 'G2':
        ness_GateLink = Gate_Link.objects.filter(
            assin_link_to_gateway='G2').filter(Link_Status="At")
    tmp_batch = []
    tmp_total_count = 0
    for kkk1 in batch:
        for kkk in ness_GateLink:
            if kkk1.link_name == kkk.Link_Name:
                tmp_batch.append(kkk1)
                tmp_total_count += 1

    pp.pprint(tmp_total_count)
    context = {
        'underMaintainance': underMaintainance,
        'status': status,
        'pk': m_pk,
        'about': about,
        "nes_gateLink": ness_GateLink,
        'batch': tmp_batch,
        'gate': gate,
        'total_batch': tmp_total_count,
        'balance': user.balance
    }
    html_template = loader.get_template('home/gate_about.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


pb_format_array = [""]


@login_required(login_url="/login/")
def gate_link(request, pk):
    onMaintainance = False

    pp = pprint.PrettyPrinter(indent=4)
    GateLink = Gate_Link.objects.filter()
    tmp_gate = Gate.objects.all()

    gm1 = Gate1Manage.objects.all()

    if GateLink.get(id=pk).Link_Status == "Hd":
        onMaintainance = True
        return redirect("/index")

    if len(gm1) > 0 and gm1[0].Gate_status == "um" and GateLink.get(id=pk).assin_link_to_gateway == "G1":
        onMaintainance = True
        return redirect("/gate_about/G1")
    gm2 = Gate2Manage.objects.all()
    if len(gm2) > 0 and gm2[0].Gate_status == "um" and GateLink.get(id=pk).assin_link_to_gateway == "G2":
        onMaintainance = True
        return redirect("/gate_about/G2")

    name = GateLink.get(id=pk).Link_Name
    cost = GateLink.get(id=pk).Link_price
    logo = GateLink.get(id=pk).Link_Logo_large
    seleted_item = GateLink.get(id=pk).Link_Selected_Item
    link_format_tmp = GateLink.get(id=pk).Link_Fomart.all()
    tmp_batch = Batch.objects.filter(
        user=str(request.user)).order_by('start_time').all()

    # for index in range(len(link_format_tmp)):
    #    link_format={"id":index,"key":link_format_tmp[index]}
    #    pp.pprint(index)
    user = balance.objects.get(user=request.user)
    context = {
        'segment': "gate_link",
        'Name': name,
        'Cost': cost,
        'Gate': tmp_gate,
        'Batch': tmp_batch,
        'Total_Batch': tmp_batch.count(),
        'logo': logo,
        'balance': user.balance,
        'link_format': link_format_tmp,
        'seleted_item': seleted_item
    }
    pp.pprint(context["seleted_item"])
    html_template = loader.get_template('home/gate_link.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


@login_required(login_url="/login/")
def area_code(request):
    context = {}
    form = AreaCodeForm(request.POST or None)
    found_cnt = 0
    not_found_cnt = 0
    error = False
    error_msg = ""
    pp = pprint.PrettyPrinter(indent=4)
    user = balance.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            if form.is_valid():
                if request.POST['area_inputData']:
                    phonenumber_arry = request.POST['area_inputData'].strip().split(
                        "\r\n")
                    if len(phonenumber_arry) > 50:
                        error = True
                        error_msg = "Area Codes Lookup up to 50 phone numbers."
                    tmp_area_array = []
                    tmp_find_result = []
                    tmp_find_result_exist = ""
                    tmp_all_result_exist = ""
                    for pn in phonenumber_arry[0:50]:
                        tmp_area = ""
                        # pp.pprint(mid(pn,i,3).isnumeric)
                        for i in range(len(pn)):
                            tmp_area = mid(pn, i, 6)
                            if tmp_area.isnumeric():
                                break
                        tmp_area_array.append(tmp_area)

                        if AreaCode.objects.filter(area_code=tmp_area).exists():
                            ttt = AreaCode.objects.get(area_code=tmp_area)
                            tmp_all_result_exist += pn+"\t"+ttt.area_code+"\t"+ttt.areaf1 + "\t" + \
                                ttt.areaf2 + "\t" + ttt.areaf3 + "\t"+ttt.areaf4 + "\t" + ttt.areaf5 + "\r\n"
                            tmp_find_result_exist += pn+"\t"+ttt.area_code+"\t"+ttt.areaf1 + "\t" + \
                                ttt.areaf2 + "\t" + ttt.areaf3 + "\t"+ttt.areaf4 + "\t" + ttt.areaf5 + "\r\n"
                            tmp_find_result.append(
                                [pn, ttt.area_code, ttt.areaf1, ttt.areaf2, ttt.areaf3, ttt.areaf4, ttt.areaf5])
                            found_cnt = found_cnt + 1
                        else:
                            tmp_all_result_exist += pn+"\t"+tmp_area+"\r\n"
                            tmp_find_result.append(
                                [pn, tmp_area, "NotFound", "NotFound", "NotFound", "NotFound", "NotFound"])
                            not_found_cnt += 1

                    context['segment'] = "in(p)_response"
                    context['area_array'] = tmp_area_array
                    context['phonenumber_arry'] = phonenumber_arry
                    context['in_data'] = request.POST['area_inputData'].strip()
                    context['find_result'] = tmp_find_result
                    context['found_cnt'] = found_cnt
                    context['not_found_cnt'] = not_found_cnt
                    context['fnd_result'] = tmp_find_result_exist
                    context['all_result'] = tmp_all_result_exist
                    context['error'] = error
                    context['error_msg'] = error_msg
            else:
                error = True
                error_msg = "Captcha is invalid"
        except:
            error = True
            error_msg = "Unknown error is occured"

    context = {
        **context,
        'balance': user.balance,
        'form': form,
        "error": error,
        "error_msg": error_msg
    }

    html_template = loader.get_template('home/area_code.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


@login_required(login_url="/login/")
def history(request, m_str):
    pp = pprint.PrettyPrinter(indent=4)
    tmp_array = {'Gate2', 'Gate1'}
    if(m_str == 'hgo'):
        tmp_item = 'Gate1'
    elif(m_str == 'hgt'):
        tmp_item = 'Gate2'
    pp.pprint(tmp_item)
    context = {
        'btn_array': tmp_array,
        'sel_item': tmp_item,
    }
    html_template = loader.get_template('home/history.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


@login_required(login_url="/login/")
def onlineSupport(request):
    access_logs = AccessLog.objects.filter(user=request.user).all()
    if len(access_logs) > 0:
        item = AccessLog.objects.get(user=request.user)
        item.last_ticket_time = datetime.utcnow()
        item.save()
    else:
        item = AccessLog.objects.create(user=request.user)
        item.save()

    form = CreateTicketForm()
    user = balance.objects.get(user=request.user)
    sm = site_manage.objects.all()
    if sm[0].Site_Status == "on":
        m_as = 1
    else:
        m_as = 0
    context = {
        'form': form,
        'balance': user.balance,
        'user_name': request.user,
        'Admin_Status': m_as
    }
    html_template = loader.get_template('home/onlineSupport.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


def send_message(request):
    pp = pprint.PrettyPrinter(indent=4)
    message = request.POST['message']
    user_name = request.POST['user']
    adminUser = User. objects. filter(is_superuser=True)

    for kk in adminUser:
        tmp_admin = kk
    pp.pprint(adminUser)
    new_message = Message.objects.create(value=message, From_User=str(
        request.user), To_User=tmp_admin, date=datetime.now())
    new_message.save()
    return JsonResponse({"messages": "123"})


def get_message(request):
    pp = pprint.PrettyPrinter(indent=4)

    messages = Message.objects.filter(
        Q(From_User=str(request.user)) | Q(To_User=request.user)).all()

    message_array = []
    for msg in messages:
        pp.pprint(msg)
        m_type = 0
        tmp_user = str(request.user)
        if msg.To_User == request.user:
            m_type = 1
            tmp_user = str(msg.From_User)
        m_tmpMSG = {
            'user': tmp_user,
            'type': m_type,
            'msg': msg.value,
            'date': msg.date
        }
        message_array.append(m_tmpMSG)
        pp.pprint(message_array)

    return JsonResponse({"messages": message_array}, safe=False)


def send_gatelink_insertdata(request):

    insertdata = request.POST['gatelink_insertdata']

    return HttpResponse("Message sent successfull")


def get_link_info(request):
    pp = pprint.PrettyPrinter(indent=4)
   # datetime.now().strftime('%H:%M:%S')
    gateLink_name = request.POST.get('gateLink_Name')

    context = {}
    m_btc = Batch.objects.filter(Q(link_name=str(gateLink_name)) & Q(
        user=str(request.user)) & Q(status="Running")).all()
    batch_array = []
    gate_array = []
    tmp_status = ""
    cnt = 0
    for btc in m_btc:
        cnt += 1
        m_gate = Gate.objects.filter(Q(gate_link_name=str(
            gateLink_name)) & Q(batch_id=btc.batch_id)).all()
        m_dicBtcItem = {
            'id': btc.id,
            'batch_id': btc.batch_id,
            'status': btc.status,
            'total': btc.total,
            'succeed': btc.succeed,
            'done': btc.done,
            'start_time': btc.start_time,
            'finish_time': btc.finish_time,
            'fail': btc.fail,
            'remains': btc.remains,
            'link_name': btc.link_name,
        }
        batch_array.append(m_dicBtcItem)
        for gat in m_gate:
            m_dicGateItem = {
                'inserted_text': gat.inserted_text,
                'result1': gat.result1,
                'result2': gat.result2,
                'result3': gat.result3,
                'result4': gat.result4,
                'result5': gat.result5,
                'status': gat.status,
                'batch_id': gat.batch_id
            }
            if len(AreaCode.objects.filter(area_code=gat.phone[0:6]).all()) > 0:
                codes = AreaCode.objects.get(area_code=gat.phone[0:6])
                m_dicGateItem["result6"] = codes.areaf1+","+codes.areaf2 + \
                    ","+codes.areaf3+","+codes.areaf4+","+codes.areaf5
            else:
                m_dicGateItem["result6"] = ""

            tmp_status += str(gat.status)
            gate_array.append(m_dicGateItem)
    context = {
        "gate": gate_array,
        "batch": batch_array,
    }
    context['str_status'] = str(cnt)
    return JsonResponse(context, safe=False)


def get_area_all(request):
    if request.POST['message'] == 'ALL':
        context = {
            "item": "all"
        }
    return JsonResponse(context)


def Gl_Send_InsertData(request):
    pp = pprint.PrettyPrinter(indent=4)

    selected_format = request.POST.get("seleted_data")
    link_name = request.POST.get("name")
    Gate_Link.objects.filter(Link_Name=link_name).update(
        Link_Selected_Item=selected_format)
    pp.pprint(selected_format)
    result = convert_format(selected_format)
    if TempFormat.objects.filter(user=request.user).exists():
        TempFormat.objects.filter(user=request.user).delete()
    new_TmpFormat = TempFormat.objects.create(user=request.user, tmpStr=result)
    new_TmpFormat.save()
    return JsonResponse({'item': 'ok'})


def GateLink_Send_Preview_Data(request):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("___________GateLink_Send_Preview_Data_____________")
    tmp_previewData = request.POST.get("gatelink_previewData_oo")
    tmp_seleted_data = request.POST.get("seleted_data")
    link_name = request.POST.get("page_name")
    Gate_Link.objects.filter(Link_Name=link_name).update(
        Link_Selected_Item=tmp_seleted_data)
    result = convert_format(tmp_seleted_data)
    if TempFormat.objects.filter(user=request.user).exists():
        TempFormat.objects.filter(user=request.user).delete()
    new_TmpFormat = TempFormat.objects.create(user=request.user, tmpStr=result)
    new_TmpFormat.save()
    pp.pprint(tmp_previewData)
    if tmp_previewData != None:
        data_arry_line = tmp_previewData.split("\n")
        pp.pprint(data_arry_line)
        tmp_format_array = str(TempFormat.objects.get(
            user=request.user)).split('#')
        tmp_format_user = request.user
        i = 0
        tmp_data_array = []
        for ii in data_arry_line:
            pp.pprint("_______data_array_line_____")
            pp.pprint(ii)
            r = convert_format(ii)
            i += 1
            if r != "":
                tmp_check = check_format(
                    tmp_format_array, r.split('#'), tmp_format_user)
                tmp_data_array.append(tmp_check)
        tmp_format_array = str(TempFormat.objects.get(
            user=request.user)).split('#')
        pp.pprint(tmp_format_array)

        jsonStr = json.dumps(list(tmp_data_array))
    return JsonResponse({'data_array': tmp_data_array, 'format_array': tmp_format_array}, safe=False)


def df_selected_ticker(request):
    cnio = cnio_api.cnio()
    pm = PaymentManage.objects.all()
    apiKey = ""
    m_amount = request.POST['amount']
    m_ticker = request.POST['ticker']
    for PayMan in pm:
        apiKey = PayMan.Api_key

    cnio.api_key(apiKey)
    res = cnio.est_exchange_rate(str(m_amount), "usdttrc20", m_ticker)
    new_res = res.decode('utf-8')
    d = json.loads(new_res)

    pp = pprint.PrettyPrinter(indent=4)

    return JsonResponse(d)


def df_get_history(request):
    pp = pprint.PrettyPrinter(indent=4)
    m_trans_array = Transaction.objects.filter(
        User_Name=str(request.user)).order_by("-Deposit_Received_At")
    m_tArray = []
   # check_transaction(m_trans_array,request.user)
   # m_trans_array = Transaction.objects.filter(User_Name = str(request.user))
    for mta in m_trans_array:
        tmp = datetime.now().timestamp() - mta.Deposit_Received_At.timestamp()
        if tmp >= 7*24*3600:
            mta.delete()
        tmp_trans_array = {
            'Transaction_ID': mid(mta.Transaction_ID, 0, 8),
            'From_Ticket': mta.From_Ticket,
            'USDT_Reciver_Address': mta.USDT_Reciver_Address,
            'Amount_Recived': mta.Amount_Recived,
            'Transaction_Status': mta.Transaction_Status,
            'Deposit_Received_At': mta.Deposit_Received_At,
            'User_Balance_updated_At': mta.User_Balance_updated_At,
            'User_Name': mta.User_Name,
            'User_Balance': mta.User_Balance
        }
        m_tArray.append(tmp_trans_array)

    context = {
        'trans_array': m_tArray
    }
    return JsonResponse(context, safe=False)


def delete_history(request):
    m_type = request.POST.get('type')
    if m_type == 'Gate1':
        tmp_str = 'G1'
    elif m_type == 'Gate2':
        tmp_str = 'G2'
    m_gateLink = Gate_Link.objects.filter(assin_link_to_gateway=tmp_str)
    blocked = 0
    for mgAr in m_gateLink:
        m_btc = Batch.objects.filter(
            Q(link_name=str(mgAr.Link_Name)) & Q(user=str(request.user)) & Q(status="Finished")).order_by("-start_time").all()
        blocked = blocked + len(Batch.objects.filter(
            Q(link_name=str(mgAr.Link_Name)) & Q(user=str(request.user)) & ~Q(status="Finished")).all())
        for btc in m_btc:
            m_gate = Gate.objects.filter(Q(gate_link_name=str(
                mgAr.Link_Name)) & Q(batch_id=btc.batch_id) & Q(Q(status=2) | Q(status=3))).all()
            m_gate.delete()
        m_btc.delete()

    context = {
        "success": True,
        "blocked": blocked
    }
    return JsonResponse(context, safe=False)


def df_deposit_click(request):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("-----------------start Deposit Click-------------")
    cnio = cnio_api.cnio()
    pm = PaymentManage.objects.all()

    m_address = ""
    apiKey = ""
    m_time = 0.0
    for PayMan in pm:
        apiKey = PayMan.Api_key
        m_address = PayMan.USDT_ADDRESS
        m_time = PayMan.Check_for_payment_status_every * 60
    pp.pprint("____________________ADDRESS______________________")
    m_address_array = m_address.split("\r\n")
    pp.pprint(len(m_address_array))
    pp.pprint(m_address_array)
    address_number = random.randint(0, len(m_address_array)-1)
    pp.pprint(address_number)
    m_amount = request.POST['amount']
    m_ticker = request.POST['ticker']
    tmp_trans = Transaction.objects.filter(
        Q(From_Ticket=m_ticker) & Q(User_Name=str(request.user))).all()
    cnt = 0
    tmp_add = ""
    tmp_id = ""
    for k in tmp_trans:
        tmp_add = k.USDT_Reciver_Address
        tmp_id = k.Transaction_ID
        if k.Transaction_Status == "waiting":
            cnt += 1
    cnio.api_key(apiKey)
    if cnt == 0:

        res = cnio.est_exchange_rate(str(m_amount), "usdttrc20", m_ticker)
        new_res = res.decode('utf-8')
        d = json.loads(new_res)
        if d.get('error') != None:
            pp.pprint("occur error!!")
        else:
            amount = d['estimatedAmount']
            pp.pprint("____________________AMOUNT______________________")
            pp.pprint(d)
            # amount =
            result = cnio.create_transaction(
                amount, m_ticker, "usdttrc20", m_address_array[address_number])
            new_res = result.decode('utf-8')
            d = json.loads(new_res)
            pp.pprint(d)
            if d.get('error') != None:
                pp.pprint("occur error!!")
            else:
                user_balance = balance.objects.get(user=request.user).balance
                trans_obj = Transaction.objects.create(User_Name=str(
                    request.user), Transaction_ID=d['id'], User_Balance=user_balance, Transaction_Status="waiting")
                trans_obj.save()
            d['amount'] = amount
    else:
        pp.pprint(tmp_id)
        res = cnio.est_exchange_rate(str(m_amount), "usdttrc20", m_ticker)
        new_res = res.decode('utf-8')
        d = json.loads(new_res)
        if d.get('error') != None:
            pp.pprint("occur error!!")
        else:
            amount = d['estimatedAmount']

            d = {
                'error': 'Status Error',
                'amount': d['estimatedAmount'],
                'tick': m_ticker,
                'payinAddress': tmp_add
            }
    return JsonResponse(d)


def gl_copy_result(request):
    pp = pprint.PrettyPrinter(indent=4)
    m_batchID = request.POST.get('batchID')
    m_btType = request.POST.get('btType')
    m_checkArray = str(request.POST.get('seleted_data')).split("#")
    m_resultStr = ""
    m_gate = []
    pp.pprint(m_btType)
    if m_btType == '0':
        m_gate = Gate.objects.filter(batch_id=m_batchID)
    elif m_btType == '1':
        m_gate = Gate.objects.filter(Q(batch_id=m_batchID) & Q(
            status=3) & Q(result1="Approved."))
    elif m_btType == '2':
        m_gate = Gate.objects.filter(Q(batch_id=m_batchID) & Q(
            status=3) & (Q(result1="Declined.") | Q(result1="Phone Number is Valid / PUK-CODE No Match.") | Q(result1="Invalid Phone Number.") | Q(result1="Expired Phone Number.")))
    elif m_btType == '3':
        m_gate = Gate.objects.filter(
            Q(batch_id=m_batchID) & (Q(status=2)))
    for k in m_gate:
        for kk in m_checkArray:
            if kk == "DI":
                m_resultStr += k.inserted_text+";"
            elif kk == "SF1":
                m_resultStr += k.result1+";"
            elif kk == "SF2":
                m_resultStr += k.result2+";"
            elif kk == "SF3":
                m_resultStr += k.result3+";"
            elif kk == "SF4":
                m_resultStr += k.result4+";"
            elif kk == "SF5":
                m_resultStr += k.result5+";"
            elif kk == "SF6":
                if len(AreaCode.objects.filter(area_code=k.phone[0:6]).all()) > 0:
                    codes = AreaCode.objects.get(area_code=k.phone[0:6])
                    m_resultStr += codes.areaf1+","+codes.areaf2 + \
                        ","+codes.areaf3+","+codes.areaf4+","+codes.areaf5+";"
                else:
                    m_resultStr += ";"

            elif kk == "ST":
                if k.status == 0:
                    m_resultStr += "In Queue;"
                elif k.status == 1:
                    m_resultStr += "Processing;"
                elif k.status == 2:
                    m_resultStr += "Error;"
                elif k.status == 3:
                    m_resultStr += "Done;"
        m_resultStr = m_resultStr[:-1]
        m_resultStr += "\r\n"
    pp.pprint(m_checkArray)

    return JsonResponse({'result': m_resultStr})


def history_get_info(request):
    pp = pprint.PrettyPrinter(indent=4)
    m_type = request.POST.get('type')
    if m_type == 'Gate1':
        tmp_str = 'G1'
    elif m_type == 'Gate2':
        tmp_str = 'G2'
    m_gateLink = Gate_Link.objects.filter(assin_link_to_gateway=tmp_str)
    batch_array = []
    gate_array = []
    for mgAr in m_gateLink:
        m_btc = Batch.objects.filter(
            Q(link_name=str(mgAr.Link_Name)) & Q(user=str(request.user))).order_by("-start_time").all()
        for btc in m_btc:
            m_gate = Gate.objects.filter(Q(gate_link_name=str(
                mgAr.Link_Name)) & Q(batch_id=btc.batch_id)).all()
            m_dicBtcItem = {
                'batch_id': btc.batch_id,
                'status': btc.status,
                'total': btc.total,
                'succeed': btc.succeed,
                'done': btc.done,
                'start_time': btc.start_time,
                'finish_time': btc.finish_time,
                'fail': btc.fail,
                'remains': btc.remains,
                'link_name': btc.link_name,
            }
            batch_array.append(m_dicBtcItem)
            for gat in m_gate:
                m_dicGateItem = {
                    'gate_link': btc.link_name,
                    'start_time': btc.start_time,
                    'inserted_text': gat.inserted_text,
                    'result1': gat.result1,
                    'result2': gat.result2,
                    'result3': gat.result3,
                    'result4': gat.result4,
                    'result5': gat.result5,
                    'status': gat.status,
                    'batch_id': gat.batch_id
                }
                gate_array.append(m_dicGateItem)

    context = {
        'batch_array': batch_array,
        'gate_array': gate_array,
    }
    return JsonResponse(context, safe=False)


def check_transaction(m_trans_array, user):
    pp = pprint.PrettyPrinter(indent=4)
    cnio = cnio_api.cnio()
    pm = PaymentManage.objects.all()
    apiKey = ""
    for PayMan in pm:
        apiKey = PayMan.Api_key

    cnio.api_key(apiKey)
    pp.pprint("worker thread checking status")
    for mta in m_trans_array:
        if mta.Transaction_Status != "finished":
            t_id = mta.Transaction_ID
            # try:
            result = cnio.get_transaction_status(t_id)
            new_res = result.decode('utf-8')
            json_res = json.loads(new_res)
            m_trans_array.filter(Transaction_ID=t_id).update(
                Deposit_Received_At=json_res['createdAt'], User_Balance_updated_At=json_res['updatedAt'])
            m_trans_array.filter(Transaction_ID=t_id).update(
                From_Ticket=json_res['fromCurrency'], USDT_Reciver_Address=json_res["payinAddress"], Transaction_Status=json_res["status"])
            if json_res['status'] == "finished":
                tmp_bb = balance.objects.filter(user=user)
                for kk in tmp_bb:
                    m_balance = float(kk.balance) + \
                        float(json_res['amountReceive'])
                balance.objects.filter(user=user).update(balance=m_balance)
                m_trans_array.filter(Transaction_ID=t_id).update(
                    Amount_Recived=json_res['amountReceive'], User_Balance=m_balance)
            # except requests.exceptions.ConnectTimeout:
            #   pp.pprint("Error ConnectTimeout")
            pp.pprint(json_res)


def addBatch(gateLinkName, value, user):
    pp = pprint.PrettyPrinter(indent=4)
    check = value.split("$$$")
    pp.pprint("_______real_data__________")

    pp.pprint(check)
    tmp_arry = str(TempFormat.objects.get(user=user)).split('#')
    tmp_batch_id = int(check_BatchID())+1
    default_array = {'phone': '0', 'DD': '0', 'MM': '0', 'YY': '0', 'string1': '#', 'string2': '#',
                     'string3': '#', 'string4': '#', 'string5': '#', 'string6': '#', 'string7': '#', 'string8': '#',
                     'string9': '#', 'string10': '#', 'batch_id': '0'}
    cnt1 = 0
    for i in check:
        temp_inserted_data_str = i.split("##")[0]
        temp_inserted_data_list = temp_inserted_data_str.split("*#*")
        temp_inserted_data_str = " ".join(temp_inserted_data_list)
        #____check inlcude space in inserted data format_____#
        tmp_y = i.split("##")[1].split('#')
        pp.pprint(temp_inserted_data_str)
        pp.pprint(tmp_y)
        tmp_xx = 0
        for ii in tmp_y:

            if ii == "":
                tmp_y.pop(tmp_xx)
            tmp_xx += 1
        pp.pprint(tmp_y)
        if len(tmp_y) == len(tmp_arry):
            pp.pprint("_____________________NO ERROR______________")
            cnt1 += 1
            cnt = 0
            for ii in tmp_y:
                default_array[tmp_arry[cnt]] = ii.strip()
                cnt += 1
            new_gate = Gate.objects.create(
                phone=default_array['phone'],
                DD=default_array['DD'],
                MM=default_array['MM'],
                YY=default_array['YY'],
                string1=default_array['string1'],
                string2=default_array['string2'],
                string3=default_array['string3'],
                string4=default_array['string4'],
                string5=default_array['string5'],
                string6=default_array['string6'],
                string7=default_array['string7'],
                string8=default_array['string8'],
                string9=default_array['string9'],
                string10=default_array['string10'],
                gate_link_name=gateLinkName,
                batch_id=tmp_batch_id,
                inserted_text=temp_inserted_data_str,
                user=str(user)

            )
            new_gate.save()

            if Gate.objects.filter(gate_link_name='#').exists():
                Gate.objects.filter(gate_link_name='#').delete()
    pp.pprint("---------Create Batch Test------------")
    if cnt1 != 0:
        new_Batch = Batch.objects.create(
            total=cnt1,
            batch_id=tmp_batch_id,
            link_name=gateLinkName,
            user=str(user),
            start_time=datetime.now(),
            finish_time=datetime.now(),
            status="Running"
        )
        new_Batch.save()


def gateLink_get_batch_data(request):
    pp = pprint.PrettyPrinter(indent=4)
    batch_array = []
    gate_array = []
    m_type = request.POST.get('type')
    pp.pprint(m_type)
    gateLink_name = request.POST.get('name')
    m_batch_id = request.POST.get('batch_id')
    if m_type == '0':
        pp.pprint(gateLink_name)

    elif m_type == '1':
        Batch.objects.filter(batch_id=int(m_batch_id)).update(
            status="Stopped", finish_time=datetime.now())
        Gate.objects.filter(Q(batch_id=int(m_batch_id)) & (
            Q(status=0) | Q(status=1))).all().update(status=2)

    elif m_type == '2':
        Batch.objects.filter(batch_id=int(m_batch_id)).update(status="Running")
        Gate.objects.filter(Q(batch_id=int(m_batch_id)) &
                            Q(status=2)).all().update(status=0)

    elif m_type == '3':
        Batch.objects.filter(batch_id=int(m_batch_id)).update(status="Running")
        Gate.objects.filter(Q(batch_id=int(m_batch_id)) &
                            Q(status=2)).all().update(status=0)
    elif m_type == '4':
        addBatch(gateLink_name, m_batch_id, request.user)
        pp.pprint(m_batch_id)
    m_btc = Batch.objects.filter(Q(link_name=str(gateLink_name)) & Q(
        user=str(request.user))).order_by("-start_time").all()
    m_runBath_array = ""
    for btc in m_btc:
        m_gate = Gate.objects.filter(Q(gate_link_name=str(
            gateLink_name)) & Q(batch_id=btc.batch_id)).all()
        m_dicBtcItem = {
            'batch_id': btc.batch_id,
            'status': btc.status,
            'total': btc.total,
            'succeed': btc.succeed,
            'done': btc.done,
            'start_time': btc.start_time,
            'finish_time': btc.finish_time,
            'fail': btc.fail,
            'remains': btc.remains,
            'retry': btc.retry,
            'link_name': btc.link_name,
        }
        batch_array.append(m_dicBtcItem)
        for gat in m_gate:

            m_dicGateItem = {
                'inserted_text': gat.inserted_text,
                'result1': gat.result1,
                'result2': gat.result2,
                'result3': gat.result3,
                'result4': gat.result4,
                'result5': gat.result5,
                'status': gat.status,
                'batch_id': gat.batch_id
            }
            if len(AreaCode.objects.filter(area_code=gat.phone[0:6]).all()) > 0:
                codes = AreaCode.objects.get(area_code=gat.phone[0:6])
                m_dicGateItem["result6"] = codes.areaf1+","+codes.areaf2 + \
                    ","+codes.areaf3+","+codes.areaf4+","+codes.areaf5
            else:
                m_dicGateItem["result6"] = ""

            gate_array.append(m_dicGateItem)
    # m_gate = Gate.objects.filter(gate_link_name = mgAr.Link_Name)
    # m_gateLink = Gate_Link.objects.filter(assin_link_to_gateway = tmp_str)
    # pp.pprint(m_gateLink)
    """
    for mgAr in m_gateLink:
        m_btc  =  Batch.objects.filter(link_name =  mgAr.Link_Name)
        m_gate = Gate.objects.filter(gate_link_name = mgAr.Link_Name)
        for btc in m_btc:
            m_dicBtcItem = {
                'batch_id':btc.batch_id,
                'status':btc.status,
                'total':btc.total,
                'succeed':btc.succeed,
                'done':btc.done,
                'start_time':btc.start_time,
                'finish_time':btc.finish_time,
                'fail':btc.fail,
                'remains':btc.remains,
                'link_name':btc.link_name,
            }
            batch_array.append(m_dicBtcItem)
        for gat in m_gate:
            m_dicGateItem = {
                'di':gat.inserted_text,
                'sf1':gat.result1,
                'sf2':gat.result2,
                'sf3':gat.result3,
                'sf4':gat.result4,
                'sf5':gat.result5,
                'st':gat.status,
                'bi':gat.batch_id
            }
            gate_array.append(m_dicGateItem)
    """
    context = {
        'batch_array': batch_array,
        'gate_array': gate_array,
        'runnig_array': m_runBath_array
    }
    pp.pprint(m_runBath_array)

    return JsonResponse(context, safe=False)
# class Transaction(models.Model):
 #   Deposit_Received_At = models.DateTimeField(blank=True)
  #  User_Balance_updated_At = models.DateTimeField(blank=True)


def download_selected_batches(request):
    result = ""
    for v in request.GET["selected_batch_ids"].split(","):
        batch = Batch.objects.get(batch_id=v)
        result += batch.link_name + "\r\n"
        gates = Gate.objects.filter(batch_id=v).all()
        for gate in gates:
            result += gate.inserted_text + "\t" + \
                gate.result1 + "\t" + \
                gate.result2 + "\t" + \
                gate.result3 + "\t" + \
                gate.result4 + "\t" + \
                gate.result5 + "\t"
            if gate.status == 0:
                result += "In Queue"
            elif gate.status == 1:
                result += "Processing"
            elif gate.status == 2:
                result += "Error"
            else:
                result += "Done"
            result += "\r\n"

    response = HttpResponse(result)
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=' + \
        batch.link_name+"_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.txt'
    return response


def delete_selected_batches(request):
    for v in request.POST["selected_batch_ids"].split(","):
        if v == "":
            break
        Batch.objects.get(batch_id=v).delete()
        Gate.objects.filter(batch_id=v).delete()
    return JsonResponse({"success": True})
