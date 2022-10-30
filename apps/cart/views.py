from functools import reduce
import os
from decimal import Decimal
from datetime import datetime, date
from urllib.request import Request
from operator import or_

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
from django.db.models import F, Q, Count, Sum
from django.utils import timezone
from django.db import transaction

from apps.home.models import balance
from apps.home.views import get_default_page_context
from apps.home.models import AreaCode
from .forms import CreateSupplierForm
from .models import *
from .serializers import *

# Create your views here.
@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def search(request):
    if request.method == 'GET':
        product_list = Shop_data.objects.all()
        batch_list = Batch.objects.raw('SELECT cart_batch.id, cart_batch.Name, (SELECT count(*) FROM cart_shop_data WHERE Batch_id=cart_batch.id AND Sold_unsold="UNSOLD") AS product_num FROM cart_batch ORDER BY id DESC')
        context = {
            'product_list': product_list,
            'batch_list': batch_list
        }
        html_template = loader.get_template('search.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                object = request.POST.get('object')
                query = Shop_data.objects.filter(Sold_unsold='UNSOLD')
                if object == 'batch':
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list)
                    data_query = query.exclude(Areaf1='Other').values('Areaf1').all().annotate(product_num=Count('Areaf1')).order_by('Areaf1')
                    other_query = query.filter(Areaf1='Other').values('Areaf1').all().annotate(product_num=Count('Areaf1'))
                    areaf1_list = Areaf1Serializer(data_query, many=True).data + Areaf1Serializer(other_query, many=True).data
                    # query = Shop_data.objects.filter(Batch__in=batch_list).values('Areaf1').distinct().all()
                    # areaf1_list = [{ 'Areaf1': each['Areaf1'], 'product_num': Shop_data.objects.aggregate(product_num=Count('Areaf1', filter=Q(Areaf1=each['Areaf1'])))['product_num'] } for each in query]
                    # query = Shop_data.objects.filter(Batch__in=batch_list).values('Zipcode').distinct().order_by('-id').all()[:50]
                    # zipcode_list = [{ 'Zipcode': each['Zipcode'] } for each in query]
                    # query = Shop_data.objects.filter(Batch__in=batch_list).values('Area_code').distinct().all()[:150]
                    # area_code_list = [{ 'Area_code': each['Area_code'] } for each in query]
                    data = {
                        'areaf1_list': areaf1_list,
                        # 'zipcode_list': zipcode_list,
                        # 'area_code_list': area_code_list
                    }
                elif object == 'areaf1':
                    areaf1_list = request.POST.getlist('areaf1_list[]')
                    areaf1_list = list(map(str, areaf1_list))
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list)
                    data_query = query.exclude(Areaf2='Other').values('Areaf2').all().annotate(product_num=Count('Areaf2')).order_by('Areaf2')
                    other_query = query.filter(Areaf2='Other').values('Areaf2').all().annotate(product_num=Count('Areaf2'))
                    areaf2_list = Areaf2Serializer(data_query, many=True).data + Areaf2Serializer(other_query, many=True).data
                    data = {
                        'areaf2_list': areaf2_list,
                    }
                elif object == 'areaf2':
                    areaf2_list = request.POST.getlist('areaf2_list[]')
                    areaf2_list = list(map(str, areaf2_list))
                    areaf1_list = request.POST.getlist('areaf1_list[]')
                    areaf1_list = list(map(str, areaf1_list))
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list)
                    data_query = query.exclude(Areaf3='Other').values('Areaf3').all().annotate(product_num=Count('Areaf3')).order_by('Areaf3')
                    other_query = query.filter(Areaf3='Other').values('Areaf3').all().annotate(product_num=Count('Areaf3'))
                    areaf3_list = Areaf3Serializer(data_query, many=True).data + Areaf3Serializer(other_query, many=True).data
                    data = {
                        'areaf3_list': areaf3_list,
                    }
                elif object == 'areaf3':
                    areaf3_list = request.POST.getlist('areaf3_list[]')
                    areaf3_list = list(map(str, areaf3_list))
                    areaf2_list = request.POST.getlist('areaf2_list[]')
                    areaf2_list = list(map(str, areaf2_list))
                    areaf1_list = request.POST.getlist('areaf1_list[]')
                    areaf1_list = list(map(str, areaf1_list))
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list)
                    data_query = query.exclude(Areaf4='Other').values('Areaf4').all().annotate(product_num=Count('Areaf4')).order_by('Areaf4')
                    other_query = query.filter(Areaf4='Other').values('Areaf4').all().annotate(product_num=Count('Areaf4'))
                    areaf4_list = Areaf4Serializer(data_query, many=True).data + Areaf4Serializer(other_query, many=True).data
                    data = {
                        'areaf4_list': areaf4_list,
                    }
                elif object == 'areaf4':
                    areaf4_list = request.POST.getlist('areaf4_list[]')
                    areaf4_list = list(map(str, areaf4_list))
                    areaf3_list = request.POST.getlist('areaf3_list[]')
                    areaf3_list = list(map(str, areaf3_list))
                    areaf2_list = request.POST.getlist('areaf2_list[]')
                    areaf2_list = list(map(str, areaf2_list))
                    areaf1_list = request.POST.getlist('areaf1_list[]')
                    areaf1_list = list(map(str, areaf1_list))
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list)
                    data_query = query.exclude(Areaf5='Other').values('Areaf5').all().annotate(product_num=Count('Areaf5')).order_by('Areaf5')
                    other_query = query.filter(Areaf5='Other').values('Areaf5').all().annotate(product_num=Count('Areaf5'))
                    areaf5_list = Areaf5Serializer(data_query, many=True).data + Areaf5Serializer(other_query, many=True).data
                    data = {
                        'areaf5_list': areaf5_list,
                    }
                elif object == 'areaf5':
                    areaf5_list = request.POST.getlist('areaf5_list[]')
                    areaf5_list = list(map(str, areaf5_list))
                    areaf4_list = request.POST.getlist('areaf4_list[]')
                    areaf4_list = list(map(str, areaf4_list))
                    areaf3_list = request.POST.getlist('areaf3_list[]')
                    areaf3_list = list(map(str, areaf3_list))
                    areaf2_list = request.POST.getlist('areaf2_list[]')
                    areaf2_list = list(map(str, areaf2_list))
                    areaf1_list = request.POST.getlist('areaf1_list[]')
                    areaf1_list = list(map(str, areaf1_list))
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).filter(Areaf5__in=areaf5_list)
                    data_query = query.exclude(State='Other').values('State').all().annotate(product_num=Count('State')).order_by('State')
                    other_query = query.filter(State='Other').values('State').all().annotate(product_num=Count('State'))
                    state_list = StateSerializer(data_query, many=True).data + StateSerializer(other_query, many=True).data
                    data = {
                        'state_list': state_list,
                    }
                elif object == 'state':
                    state_list = request.POST.getlist('state_list[]')
                    state_list = list(map(str, state_list))
                    areaf5_list = request.POST.getlist('areaf5_list[]')
                    areaf5_list = list(map(str, areaf5_list))
                    areaf4_list = request.POST.getlist('areaf4_list[]')
                    areaf4_list = list(map(str, areaf4_list))
                    areaf3_list = request.POST.getlist('areaf3_list[]')
                    areaf3_list = list(map(str, areaf3_list))
                    areaf2_list = request.POST.getlist('areaf2_list[]')
                    areaf2_list = list(map(str, areaf2_list))
                    areaf1_list = request.POST.getlist('areaf1_list[]')
                    areaf1_list = list(map(str, areaf1_list))
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).filter(Areaf5__in=areaf5_list).filter(State__in=state_list)
                    data_query = query.exclude(City='Other').values('City').all().annotate(product_num=Count('City')).order_by('City')
                    other_query = query.filter(City='Other').values('City').all().annotate(product_num=Count('City'))
                    city_list = CitySerializer(data_query, many=True).data + CitySerializer(other_query, many=True).data
                    data = {
                        'city_list': city_list,
                    }
                returnData = {
                    'state': 'OK',
                    'data': data
                }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)



# Create your views here.
@login_required(login_url="/login/")
@require_http_methods(["POST"])
def search_result(request):
    if request.is_ajax():
        try:
            # search by batch
            batch_list = request.POST.getlist('batch_list[]')
            if len(batch_list):
                query = Shop_data.objects.filter(Batch__in=batch_list)
                # search by gender
                gender_list = request.POST.getlist('gender_list[]')
                if len(gender_list):
                    query = query.filter(Gender__in=gender_list)
                    # search by price
                    price_min = request.POST.get('price_min')
                    price_max = request.POST.get('price_max')
                    if price_min == '':
                        price_min = 0
                    else:
                        price_min = float(price_min.split(' ')[1])
                    if price_max == '':
                        price_max = 0
                    else:
                        price_max = float(price_max.split(' ')[1])
                    if price_min == 0 and price_max == 0:
                        pass
                    else:
                        query = query.filter(Price__range=[price_min, price_max])
                    #search by extra
                    extra1 = request.POST.get('extra1')
                    if extra1=='true':
                        query = query.filter(Extra1__isnull=False).exclude(Extra1='')
                    extra2 = request.POST.get('extra2')
                    if extra2=='true':
                        query = query.filter(Extra2__isnull=False).exclude(Extra2='')
                    extra3 = request.POST.get('extra3')
                    if extra3=='true':
                        query = query.filter(Extra3__isnull=False).exclude(Extra3='')
                    extra4 = request.POST.get('extra4')
                    if extra4=='true':
                        query = query.filter(Extra4__isnull=False).exclude(Extra4='')
                    extra5 = request.POST.get('extra5')
                    if extra5=='true':
                        query = query.filter(Extra5__isnull=False).exclude(Extra5='')
                    query = query.filter(Sold_unsold='UNSOLD')
                    #search by area code
                    area_code_list = request.POST.getlist('area_code_list[]')
                    area_code_list = [each[:6] for each in area_code_list]
                    if len(area_code_list):
                        print(area_code_list)
                        query = query.filter(Area_code__in=area_code_list)
                        product_list = query.order_by('-id').all()
                    else:
                        zipcode_list = request.POST.getlist('zipcode_list[]')
                        if len(zipcode_list):
                            filter = []
                            for zipcode in zipcode_list:
                                filter.append(Q(Zipcode__contains=zipcode))
                            query = query.filter(reduce(or_, filter))
                            product_list = query.order_by('-id').all()
                        else:
                            areaf1_list = request.POST.getlist('areaf1_list[]')
                            areaf2_list = request.POST.getlist('areaf2_list[]')
                            areaf3_list = request.POST.getlist('areaf3_list[]')
                            areaf4_list = request.POST.getlist('areaf4_list[]')
                            areaf5_list = request.POST.getlist('areaf5_list[]')
                            state_list = request.POST.getlist('state_list[]')
                            city_list = request.POST.getlist('city_list[]')
                            if len(city_list):
                                query = query.filter(City__in=city_list)
                            if len(state_list):
                                query = query.filter(State__in=state_list)
                            if len(areaf5_list):
                                query = query.filter(Areaf5__in=areaf5_list)
                            if len(areaf4_list):
                                query = query.filter(Areaf4__in=areaf4_list)
                            if len(areaf3_list):
                                query = query.filter(Areaf3__in=areaf3_list)
                            if len(areaf2_list):
                                query = query.filter(Areaf2__in=areaf2_list)
                            if len(areaf1_list):
                                query = query.filter(Areaf1__in=areaf1_list)
                            print(repr(query.count()))
                            product_list = query.order_by('-id').all()
                    
                    data = ProductSerializer(product_list, many=True).data
                    page = int(request.POST.get('page'))
                    ############### ? Pagination ##################
                    data_length = len(data)
                    start = page * 10
                    end = min((page + 1) * 10, data_length + 1)
                    data = data[start:end]
                    ##############################################
                    returnData = {
                        'state': 'OK',
                        'data': data,
                        'length': data_length
                    }
                else:
                    returnData = {
                        'state': "FAIL",
                        'error': "Please select the gender"
                    }
            else:
                returnData = {
                    'state': "FAIL",
                    'error': "Please select the batch"
                }
        except Exception as e:
            returnData = {
                'state': "FAIL",
                'error': repr(e)
            }
        return JsonResponse(returnData)

        
@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
@transaction.atomic
def cart_home(request):
    if request.method == 'GET':
        cart_obj = Cart.objects.new_or_get(request)
        checker_list = Checker.objects.all()
        context = {
            'count_product': cart_obj.products.count(),
            'checker_list': checker_list
        }
        html_template = loader.get_template('shoping_cart.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                cart_obj = Cart.objects.new_or_get(request)
                type = request.POST.get('type')
                if type == 'get':
                    query = cart_obj.products.order_by('-id').all()
                    data = ProductSerializer(query, many=True).data
                elif type == 'remove':
                    product_id = int(request.POST.get('product_id', None))
                    product_obj = Shop_data.objects.get(id=product_id)
                    if product_obj.Sold_unsold == 'CHECKING':                    
                        returnData = {
                            'state': 'Error',
                            'error': "This item is checking now."
                        }
                        return JsonResponse(returnData)
                    if cart_obj.products.filter(pk=product_obj.pk).exists():
                        product_obj.Sold_unsold = 'UNSOLD'
                        product_obj.User = None
                        product_obj.save()
                        cart_obj.products.remove(product_obj)
                        balance_obj = balance.objects.get(user=request.user)
                        balance_obj.balance = round(balance_obj.balance + float(product_obj.Price), 2)
                        balance_obj.save()
                        data = {
                            'balance': balance_obj.balance,
                            'count_product': cart_obj.products.count()
                        }
                    else:
                        returnData = {
                            'state': "FAIL",
                            'error': "This item has already removed from cart."
                        }
                        return JsonResponse(returnData)

                elif type == 'add':
                    product_id = int(request.POST.get('product_id', None))
                    product_obj = Shop_data.objects.get(id=product_id)
                    if product_obj.Sold_unsold == 'CHECKING':                    
                        returnData = {
                            'state': 'Error',
                            'error': "This item is checking now."
                        }
                        return JsonResponse(returnData)
                    if cart_obj.products.filter(pk=product_obj.pk).exists():
                        returnData = {
                            'state': "FAIL",
                            'error': "This item has already added to cart."
                        }
                        return JsonResponse(returnData)
                    if product_obj.Sold_unsold == 'ON_CART':
                        returnData = {
                            'state': "FAIL",
                            'error': "This item has already sold."
                        }
                        return JsonResponse(returnData)
                    balance_obj = balance.objects.get(user=request.user)
                    if float(product_obj.Price) > balance_obj.balance:
                        data = {
                            'over_balance': True
                        }
                    else:
                        cart_obj.products.add(product_obj)
                        product_obj.Sold_unsold = 'ON_CART'
                        product_obj.User = request.user
                        product_obj.save()
                        balance_obj = balance.objects.get(user=request.user)
                        balance_obj.balance = round(balance_obj.balance - float(product_obj.Price), 2)
                        balance_obj.save()
                        data = {
                            'over_balance': False,
                            'balance': balance_obj.balance,
                            'count_product': cart_obj.products.count()
                        }

                returnData = {
                    'state': 'OK',
                    'data': data
                }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)

        
@login_required(login_url="/login/")
@require_http_methods(["POST"])
def check_product(request):
    if request.is_ajax():
        try:
            checker_id = int(request.POST.get('checker_id', None))
            product_id = int(request.POST.get('product_id', None))                    
            cart_obj = Cart.objects.new_or_get(request)
            product_obj = Shop_data.objects.get(id=product_id)

            if cart_obj.products.filter(pk=product_obj.pk).exists():
                
                balance_obj = balance.objects.get(user=request.user)
                checker_obj = Checker.objects.get(id=checker_id)
                if balance_obj.balance < float(checker_obj.Cost):                
                    returnData = {
                        'state': 'Over_balance',
                    }
                    return JsonResponse(returnData)
                if product_obj.Sold_unsold == 'CHECKING':                    
                    returnData = {
                        'state': 'Error',
                        'error': "This item is checking now."
                    }
                    return JsonResponse(returnData)
                product_obj.Sold_unsold = 'CHECKING'
                product_obj.save()
                print('Checking...')
                check_status = checker_api(product_id, checker_id, request.user.id)
                check_status = check_status[:-1]
                print(check_status)
        
                if (check_status == "phone registered successfully" or check_status == "Registration success" or check_status == "Thank you for your Registration"):
                    # print("_________________DONE__________________")
                    checker_response_text = check_status
                    checker_response_full = "Phone Registered Successfully"
                    check_status = "Done"
                elif (check_status == "Phone Registration Fails ." or check_status == "Phone number is no more active." or check_status == "Please check your phone number."):
                    # print("_________________FAIL__________________")
                    checker_response_text = check_status
                    checker_response_full = "Phone Registration Fails"
                    check_status = "Fail"
                elif (check_status == "Please try again " or check_status == "Please try again later" or check_status == "Problem while processing your request. " or check_status == "Can’t process your request at the moment" or check_status == "Service is over load please try again later"):
                    # print("__________________ERROR_________________")
                    checker_response_text = check_status
                    checker_response_full = "Please try again Later"
                    check_status = "Error"
                else:
                    # print("__________________UNKOWN ERROR_________________")
                    checker_response_text = check_status
                    checker_response_full = "Unknown error please contact support"
                    check_status = "Error"

                with transaction.atomic():
                    if check_status == 'Done':
                        product_obj.Sold_unsold = 'SOLD'
                        product_obj.User = request.user
                        product_obj.Sold_date = timezone.now()
                        product_obj.save()
                        new_history = Order_history(
                            User=request.user,
                            Product=product_obj,
                            Checker=checker_obj,
                            Checker_status=check_status,
                            Checker_response_text=checker_response_text,
                            Checker_response_full=checker_response_full,
                        )
                        new_history.save()
                        balance_obj = balance.objects.get(user=request.user)
                        balance_obj.balance = round(balance_obj.balance - float(checker_obj.Cost), 2)
                        balance_obj.save()
                        returnData = {
                            'state': check_status,
                        }
                        cart_obj.products.remove(product_obj)
                    elif check_status == 'Fail':
                        product_obj.Sold_unsold = 'REFUND'
                        product_obj.User = request.user
                        product_obj.Sold_date = timezone.now()
                        product_obj.save()
                        new_history = Order_history(
                            User=request.user,
                            Product=product_obj,
                            Checker=checker_obj,
                            Checker_status=check_status,
                            Checker_response_text=checker_response_text,
                            Checker_response_full=checker_response_full,
                        )
                        new_history.save()
                        balance_obj = balance.objects.get(user=request.user)
                        balance_obj.balance = round(balance_obj.balance - float(checker_obj.Cost) + float(product_obj.Price), 2)
                        balance_obj.save()
                        returnData = {
                            'state': check_status,
                            'error': "This is Invalid Phone. This item price has been refuned to your balance."
                        }
                        cart_obj.products.remove(product_obj)
                    else:
                        product_obj.Sold_unsold = 'ON_CART'
                        product_obj.save()
                        returnData = {
                            'state': check_status,
                            'error': "Problem while checking your Phone. Please try again or select a differant checker."
                        }

                balance_obj = balance.objects.get(user=request.user)
                data = {
                    'balance': balance_obj.balance,
                    'count_product': cart_obj.products.count()
                }
                returnData['data'] = data
            else:
                returnData = {
                    'state': "Error",
                    'error': "This item has already removed from cart."
                }
                return JsonResponse(returnData)
        except Exception as e:
            if product_obj.Sold_unsold == 'CHECKING':
                product_obj.Sold_unsold = 'ON_CART'
                product_obj.save()
            returnData = {
                'state': 'Error',
                'error': "Problem while checking your Phone. Please try again or select a differant checker."
            }
        return JsonResponse(returnData)

        
@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def order_history(request):
    if request.method == 'GET':
        cart_obj = Cart.objects.new_or_get(request)
        context = {
            'count_product': cart_obj.products.count()
        }
        html_template = loader.get_template('order_history.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                query = Order_history.objects.filter(User=request.user).filter(Checker_status='Done').order_by('-id').all()
                data = HistorySerializer(query, many=True).data
                page = int(request.POST.get('page'))
                ############### ? Pagination ##################
                data_length = len(data)
                start = page * 10
                end = min((page + 1) * 10, data_length + 1)
                data = data[start:end]
                ##############################################
                returnData = {
                    'state': "OK",
                    'data': data,
                    'length': data_length
                }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)


@transaction.non_atomic_requests(using='other')
def checker_api(product_id, checker_id, user_id):
    checker_name = Checker.objects.get(id=checker_id).Name + '.py'
    command = 'python3 %s %d %d %d' % (checker_name, product_id, checker_id, user_id)
    file_name = 'tmp' + str(product_id)
    os.system(command + ' > ' + file_name)
    result = open(file_name, 'r').read()
    os.remove(file_name)
    return result

        
@login_required(login_url="/login/")
@require_http_methods(["GET"])
def store_info_view(request):
    store_info = StoreInfoManage.objects.first()
    context = {
        'store_info': store_info,
    }
    html_template = loader.get_template('store_info.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))


@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
@transaction.atomic
def insert_batch(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_superuser == 0:
        return redirect(reverse('login'))
    if request.method == 'GET':
        supplier_list = Supplier.objects.all()
        context = {
            'supplier_list': supplier_list
        }
        html_template = loader.get_template('new_batch.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                batch_num = int(request.POST.get('batch_num'))
                field_list = request.POST.getlist('field_list[]')
                batch_name = request.POST.get('batch_name')
                percent = request.POST.get('percent')
                percent = int(percent.split(' ')[0])
                price = request.POST.get('price')
                price = Decimal(price.split(' ')[1])
                supplier_id = int(request.POST.get('supplier_id'))
                supplier = Supplier.objects.get(id=supplier_id)
                new_batch = Batch(Name=batch_name, Supplier=supplier, Percent=percent)
                new_batch.save()
                data = []
                duplicates = []
                for row in range(batch_num):
                    batch_list = request.POST.getlist(f'batch_list[{row}][]')
                    row_dic = {}
                    for i in range(len(field_list)):
                        if field_list[i] != 'ignore':
                            if i < len(batch_list):
                                row_dic[field_list[i]] = batch_list[i]
                    # row_dic = dict(zip(field_list, batch_list))
                    row_dic['Area_code'] = row_dic['Phone'][:6]

                    area_code_query = AreaCode.objects.filter(area_code=row_dic['Area_code'])
                    if area_code_query.exists():
                        area_code_query = area_code_query.first()
                        row_dic['Areaf1'] = area_code_query.areaf1
                        row_dic['Areaf2'] = area_code_query.areaf2
                        row_dic['Areaf3'] = area_code_query.areaf3
                        row_dic['Areaf4'] = area_code_query.areaf4
                        row_dic['Areaf5'] = area_code_query.areaf5
                        row_dic['Areaf6'] = area_code_query.areaf6
                    row_dic['Batch'] = new_batch.id
                    row_dic['Price'] = price

                    # check duplicates
                    phone_list = (Shop_data.objects.values_list('Phone', flat=True))
                    if row_dic['Phone'] in phone_list:
                        duplicates.append(row_dic)
                    else:
                        data.append(row_dic)

                many = isinstance(data, list)
                serializer = ShopDataSerializer(data=data, many=many)
                
                if serializer.is_valid(raise_exception=True):
                    serializer.save()   
                    data_length = len(data)
                    if data_length == 0 and new_batch:
                        new_batch.delete()             
                    returnData = {
                        'state': "OK",
                        'data_length': len(data),
                        'duplicates': duplicates
                    }
                else:
                    returnData = {
                        'state': "FAIL",
                        'error': serializer.errors
                    }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)

        
@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def batch_management(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_superuser == 0:
        return redirect(reverse('login'))
    if request.method == 'GET':
        supplier_list = Supplier.objects.all()
        product_query = Shop_data.objects.exclude(Sold_date=None).order_by('Sold_date')
        if product_query.exists():
            start_date = product_query.first().Sold_date.strftime('%m/%d/%Y')
            end_date = product_query.last().Sold_date.strftime('%m/%d/%Y')
        else:
            start_date = '01/01/2022'
            end_date = date.today().strftime('%m/%d/%Y')
        context = {
            'supplier_list': supplier_list,
            'start_date': start_date,
            'end_date': end_date
        }
        html_template = loader.get_template('manage_batches.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                supplier_id = int(request.POST.get('supplier_id'))
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                from_date = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
                to_date = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()
                print(from_date, to_date)
                PaidUnpaid = request.POST.get('PaidUnpaid')

                supplier_obj = Supplier.objects.get(id=supplier_id)
                batch_query = Batch.objects.filter(Supplier=supplier_obj)

                total_batches = 0
                total_sold = 0
                total_supplier_profit = 0
                total_refund = 0
                total_supplier = 1
                total_sold_price = 0
                total_shop_profit = 0
                total_unsold = 0

                tableData = []
                for batch in batch_query.all():
                    products = Shop_data.objects.filter(Batch=batch).filter(Supplier_payment_status=PaidUnpaid)
                    sold_products = products.filter(Sold_date__date__range=(from_date, to_date)).filter(Sold_unsold='SOLD')
                    refund_products = products.filter(Sold_date__date__range=(from_date, to_date)).filter(Sold_unsold='REFUND')
                    unsold_products = products.filter(Q(Sold_unsold='ON_CART') | Q(Sold_unsold='UNSOLD'))
                    row = {
                        'batch_id': batch.id,
                        'batch_name': batch.Name,
                        'supplier_name': supplier_obj.Username,
                        'supplier_batch_share': batch.Percent,
                        'total_sold': sold_products.count(),
                        'total_sold_price': sold_products.aggregate(total_price=Sum('Price'))['total_price'] or 0,
                        'total_refund': refund_products.count(),
                        'total_unsold': unsold_products.count()
                    }
                    row['total_supplier_profit'] = row['total_sold_price'] * row['supplier_batch_share'] / Decimal(100)
                    row['total_shop_profit'] = row['total_sold_price'] - row['total_supplier_profit']
                    tableData.append(row)
                    total_batches += 1
                    total_sold += row['total_sold']
                    total_sold_price += row['total_sold_price']
                    total_supplier_profit += row['total_supplier_profit']
                    total_shop_profit += row['total_shop_profit']
                    total_refund += row['total_refund']
                    total_unsold += row['total_unsold']
                data = {
                    'tableData': tableData,
                    'total_batches': total_batches,
                    'total_supplier': total_supplier,
                    'total_sold': total_sold,
                    'total_sold_price': total_sold_price,
                    'total_supplier_profit': total_supplier_profit,
                    'total_shop_profit': total_shop_profit,
                    'total_refund': total_refund,
                    'total_unsold': total_unsold
                }
                returnData = {
                    'state': "OK",
                    'data': data
                }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)

@login_required(login_url="/login/")
@require_http_methods(["POST"])
def get_batch_product_list(request):
    if request.is_ajax():
        try:
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            from_date = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
            to_date = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()
            print(from_date, to_date)
            PaidUnpaid = request.POST.get('PaidUnpaid')
            get_type = request.POST.get('type')
            batch_id = request.POST.get('batch_id')

            batch_obj = Batch.objects.get(id=batch_id)
            products = Shop_data.objects.filter(Batch=batch_obj).filter(Supplier_payment_status=PaidUnpaid)
            if get_type == 'total-sold':
                sold_product_list = products.filter(Sold_date__date__range=(from_date, to_date)).filter(Sold_unsold='SOLD').values_list('pk', flat=True)
                sold_products = Order_history.objects.filter(Product__in=sold_product_list).order_by('-Checker_date')
                data = SoldRefundSerializer(sold_products, many=True).data
            elif get_type == 'total-refund':
                refund_product_list = products.filter(Sold_date__date__range=(from_date, to_date)).filter(Sold_unsold='REFUND')
                refund_products = Order_history.objects.filter(Product__in=refund_product_list).filter(Product__Supplier_payment_status=PaidUnpaid).filter(Checker_date__range=(from_date, to_date)).filter(Product__Sold_unsold='REFUND').order_by('-Checker_date')
                data = SoldRefundSerializer(refund_products, many=True).data
            elif get_type == 'total-unsold':
                unsold_products = Shop_data.objects.filter(Batch=batch_obj).filter(Supplier_payment_status=PaidUnpaid).filter(Q(Sold_unsold='ON_CART') | Q(Sold_unsold='UNSOLD')).order_by('-Sold_date')
                data = RecordsSerializer(unsold_products, many=True).data
            page = int(request.POST.get('page'))
            ############### ? Pagination ##################
            data_length = len(data)
            start = page * 10
            end = min((page + 1) * 10, data_length + 1)
            data = data[start:end]
            ##############################################
            returnData = {
                'state': "OK",
                'data': data,
                'length': data_length
            }
        except Exception as e:
            returnData = {
                'state': "FAIL",
                'error': repr(e)
            }
        return JsonResponse(returnData)

@login_required(login_url="/login/")
@require_http_methods(["POST"])
def set_product_as_paid(request):
    if request.is_ajax():
        try:
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            from_date = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
            to_date = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()
            print(from_date, to_date)
            PaidUnpaid = request.POST.get('PaidUnpaid')
            batch_list = request.POST.getlist('batch_list[]')
            print(batch_list)

            products = Shop_data.objects.filter(Batch__in=batch_list).filter(Sold_unsold='SOLD').filter(Supplier_payment_status=PaidUnpaid).filter(Sold_date__date__range=(from_date, to_date))
            print(len(products))
            products.update(Supplier_payment_status='PAID')
            returnData = {
                'state': "OK"
            }
        except Exception as e:
            returnData = {
                'state': "FAIL",
                'error': repr(e)
            }
        return JsonResponse(returnData)
        
@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def payment_request(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_superuser == 0:
        return redirect(reverse('login'))
    if request.method == 'GET':
        context = {
        }
        html_template = loader.get_template('payment_request.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                PaidUnpaid = request.POST.get('PaidUnpaid')
                query = SupplierRequest.objects.filter(Status=PaidUnpaid).order_by('-Date').all()
                data = RequestSerializer(query, many=True).data
                page = int(request.POST.get('page'))
                ############### ? Pagination ##################
                data_length = len(data)
                start = page * 10
                end = min((page + 1) * 10, data_length + 1)
                data = data[start:end]
                ##############################################
                returnData = {
                    'state': "OK",
                    'data': data,
                    'length': data_length
                }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)
        
@login_required(login_url="/login/")
@require_http_methods(["POST"])
def set_request_as_paid(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_superuser == 0:
        return redirect(reverse('login'))
    if request.is_ajax():
        try:
            request_id = request.POST.get('request_id')
            TXID = request.POST.get('TXID')
            request_obj = SupplierRequest.objects.get(id=request_id)
            request_obj.TXID = TXID
            request_obj.Status = 'PAID'
            request_obj.save()
            returnData = {
                'state': "OK"
            }
        except Exception as e:
            returnData = {
                'state': "FAIL",
                'error': repr(e)
            }
        return JsonResponse(returnData)

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
@transaction.atomic
def create_supplier(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_superuser == 0:
        return redirect(reverse('login'))
    supplier_list = Supplier.objects.values_list('Username', flat=True)
    user_list = User.objects.exclude(username__in=supplier_list).all()
    if request.method == 'GET':
        form = CreateSupplierForm()
        context = {
            'form': form,
            'user_list': user_list
        }
    else:
        form = CreateSupplierForm(request.POST)
        context = {
            'form': form,
            'user_list': user_list
        }
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            new_supplier = Supplier(Username=username)
            new_supplier.save()
            context['form'] = CreateSupplierForm(),
            context['success'] = 'Create a new user and set it as a supplier'
    html_template = loader.get_template('manage_supplier.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
        
@login_required(login_url="/login/")
@require_http_methods(["POST"])
def set_user_as_supplier(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_superuser == 0:
        return redirect(reverse('login'))
    if request.is_ajax():
        try:
            user_id = int(request.POST.get('user_id'))
            user_obj = User.objects.get(pk=user_id)
            new_supplier = Supplier(Username=user_obj.username)
            new_supplier.save()
            returnData = {
                'state': "OK"
            }
        except Exception as e:
            returnData = {
                'state': "FAIL",
                'error': repr(e)
            }
        return JsonResponse(returnData)

    
@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def show_batch(request):
    supplier_obj = Supplier.objects.filter(Username=request.user.username)
    if supplier_obj.exists() == False:
        return redirect(reverse('login'))
    supplier_obj = supplier_obj.first()
    if request.method == 'GET':
        product_query = Shop_data.objects.order_by('Insert_date')
        if product_query.exists():
            start_date = product_query.first().Insert_date.strftime('%m/%d/%Y')
            end_date = product_query.last().Insert_date.strftime('%m/%d/%Y')
        else:
            start_date = '01/01/2022'
            end_date = date.today().strftime('%m/%d/%Y')
        context = {
            'start_date': start_date,
            'end_date': end_date
        }
        html_template = loader.get_template('manage_your_batches.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                from_date = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
                to_date = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()
                print(from_date, to_date)
                PaidUnpaid = request.POST.get('PaidUnpaid')

                batch_query = Batch.objects.filter(Supplier=supplier_obj)

                total_batches = 0
                total_sold = 0
                total_supplier_profit = 0
                total_refund = 0
                total_sold_price = 0
                total_unsold = 0

                tableData = []
                for batch in batch_query.all():
                    products = Shop_data.objects.filter(Batch=batch).filter(Supplier_payment_status=PaidUnpaid)
                    sold_products = products.filter(Sold_date__date__range=(from_date, to_date)).filter(Sold_unsold='SOLD')
                    refund_products = products.filter(Sold_date__date__range=(from_date, to_date)).filter(Sold_unsold='REFUND')
                    unsold_products = products.filter(Q(Sold_unsold='ON_CART') | Q(Sold_unsold='UNSOLD'))
                    row = {
                        'batch_id': batch.id,
                        'batch_name': batch.Name,
                        'supplier_batch_share': batch.Percent,
                        'total_sold': sold_products.count(),
                        'total_sold_price': sold_products.aggregate(total_price=Sum('Price'))['total_price'] or 0,
                        'total_refund': refund_products.count(),
                        'total_unsold': unsold_products.count()
                    }
                    row['total_supplier_profit'] = row['total_sold_price'] * row['supplier_batch_share'] / Decimal(100)
                    row['total_shop_profit'] = row['total_sold_price'] - row['total_supplier_profit']
                    tableData.append(row)
                    total_batches += 1
                    total_sold += row['total_sold']
                    total_sold_price += row['total_sold_price']
                    total_supplier_profit += row['total_supplier_profit']
                    total_refund += row['total_refund']
                    total_unsold += row['total_unsold']
                data = {
                    'tableData': tableData,
                    'total_batches': total_batches,
                    'total_sold': total_sold,
                    'total_sold_price': total_sold_price,
                    'total_supplier_profit': total_supplier_profit,
                    'total_refund': total_refund,
                    'total_unsold': total_unsold
                }
                returnData = {
                    'state': "OK",
                    'data': data
                }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def supplier_request(request):
    supplier_obj = Supplier.objects.filter(Username=request.user.username)
    if supplier_obj.exists() == False:
        return redirect(reverse('login'))
    supplier_obj = supplier_obj.first()
    if request.method == 'GET':
        context = {
        }
        html_template = loader.get_template('request_payment.html')
        return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
    else:
        if request.is_ajax():
            try:
                query = SupplierRequest.objects.filter(Supplier=supplier_obj).order_by('-Date').all()
                data = RequestSerializer(query, many=True).data
                page = int(request.POST.get('page'))
                ############### ? Pagination ##################
                data_length = len(data)
                start = page * 10
                end = min((page + 1) * 10, data_length + 1)
                data = data[start:end]
                ##############################################
                returnData = {
                    'state': "OK",
                    'data': data,
                    'length': data_length
                }
            except Exception as e:
                returnData = {
                    'state': "FAIL",
                    'error': repr(e)
                }
            return JsonResponse(returnData)

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def create_request(request):
    supplier_obj = Supplier.objects.filter(Username=request.user.username)
    if supplier_obj.exists() == False:
        return redirect(reverse('login'))
    supplier_obj = supplier_obj.first()
    if request.is_ajax():
        try:
            USDT_address = request.POST.get('USDT_address')
            if SupplierRequest.objects.filter(
                Supplier=supplier_obj.id,
                Status='UNPAID'
                ).exists():
                returnData = {
                    'state': "FAIL",
                    'error': "You aren't be able to create a new request since the last request was still marked as unpaid"
                }
            else:
                new_request = SupplierRequest(
                    Supplier=supplier_obj,
                    USDT_address=USDT_address
                    )
                new_request.save()
                returnData = {
                    'state': "OK"
                }
        except Exception as e:
            returnData = {
                'state': "FAIL",
                'error': repr(e)
            }
        return JsonResponse(returnData)