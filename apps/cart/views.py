import os
from decimal import Decimal
from datetime import datetime, date

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import F, Q, Count, Sum
from apps.home.models import balance

from apps.home.views import get_default_page_context
from apps.home.models import AreaCode
from .models import *
from .serializers import *

# Create your views here.
@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def search(request):
    if request.method == 'GET':
        product_list = Shop_data.objects.all()
        batch_list = Batch.objects.raw('SELECT cart_batch.id, cart_batch.Name, (SELECT count(*) FROM cart_shop_data WHERE Batch_id=cart_batch.id) AS product_num FROM cart_batch ORDER BY id DESC')
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
                query = Shop_data.objects.filter((Q(User=request.user) & Q(Sold_unsold='ON_CART')) | Q(Sold_unsold='UNSOLD'))
                if object == 'batch':
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = query.filter(Batch__in=batch_list).values('Areaf1').all().annotate(product_num=Count('Areaf1')).order_by('Areaf1')
                    areaf1_list = Areaf1Serializer(query, many=True).data
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
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).values('Areaf2').all().annotate(product_num=Count('Areaf2')).order_by('Areaf2')
                    areaf2_list = Areaf2Serializer(query, many=True).data
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
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).values('Areaf3').all().annotate(product_num=Count('Areaf3')).order_by('Areaf3')
                    areaf3_list = Areaf3Serializer(query, many=True).data
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
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).values('Areaf4').all().annotate(product_num=Count('Areaf4')).order_by('Areaf4')
                    areaf4_list = Areaf4Serializer(query, many=True).data
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
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).values('Areaf5').all().annotate(product_num=Count('Areaf5')).order_by('Areaf5')
                    areaf5_list = Areaf5Serializer(query, many=True).data
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
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).filter(Areaf5__in=areaf5_list).values('State').all().annotate(product_num=Count('State')).order_by('State')
                    state_list = StateSerializer(query, many=True).data
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
                    query = query.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).filter(Areaf5__in=areaf5_list).filter(State__in=state_list).values('City').all().annotate(product_num=Count('City')).order_by('City')
                    city_list = CitySerializer(query, many=True).data
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
                    print(price_min)
                    print(price_max)
                    if price_min == '':
                        price_min = 0
                    else:
                        price_min = float(price_min.split(' ')[1])
                    if price_max == '':
                        price_max = 0
                    else:
                        price_max = float(price_max.split(' ')[1])
                    print(price_min)
                    print(price_max)
                    if price_min == 0 and price_max == 0:
                        pass
                    else:
                        query = query.filter(Price__range=[price_min, price_max])
                    #search by extra
                    extra1 = request.POST.get('extra1')
                    if extra1=='true':
                        query = query.exclude(Extra1='')
                    extra2 = request.POST.get('extra2')
                    if extra2=='true':
                        query = query.exclude(Extra2='')
                    extra3 = request.POST.get('extra3')
                    if extra3=='true':
                        query = query.exclude(Extra3='')
                    extra4 = request.POST.get('extra4')
                    if extra4=='true':
                        query = query.exclude(Extra4='')
                    extra5 = request.POST.get('extra5')
                    if extra5=='true':
                        query = query.exclude(Extra5='')
                    #search by area code
                    area_code_list = request.POST.getlist('area_code_list[]')
                    area_code_list = [each[:6] for each in area_code_list]
                    if len(area_code_list):
                        print(area_code_list)
                        query = query.filter(Area_code__in=area_code_list)
                        query = query.filter((Q(User=request.user) & Q(Sold_unsold='ON_CART')) | Q(Sold_unsold='UNSOLD'))
                        product_list = query.order_by('-id').all()
                    else:
                        zipcode_list = request.POST.getlist('zipcode_list[]')
                        if len(zipcode_list):
                            # search by batch and gender
                            where = ' WHERE Batch_id IN {} AND Gender IN {}'.format(repr(tuple(batch_list)), repr(tuple(gender_list)))
                            # search by price
                            if price_min == 0 and price_max == 0:
                                pass
                            else:
                                where += ' AND Price>={} AND Price<={}'.format(price_min, price_max)
                            # search by extra
                            if extra1=='true':
                                where += ' AND Extra1!=""'
                            if extra2=='true':
                                where += ' AND Extra2!=""'
                            if extra3=='true':
                                where += ' AND Extra3!=""'
                            if extra4=='true':
                                where += ' AND Extra4!=""'
                            if extra5=='true':
                                where += ' AND Extra5!=""'
                                
                            for idx, zipcode in enumerate(zipcode_list):
                                if idx == 0:
                                    where += " AND (Zipcode LIKE '%%{}%%'".format(zipcode)
                                else:
                                    where += " OR Zipcode LIKE '%%{}%%'".format(zipcode)
                            where += ') AND (Sold_unsold="UNSOLD" OR (User_id=%d AND Sold_unsold="ON_CART"))' % (request.user.id)
                            sql = 'SELECT * FROM cart_shop_data{} ORDER BY id DESC'.format(where)
                            product_list = Shop_data.objects.raw(sql)
                            # query = query.filter(Zipcode__in=zipcode_list)
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
                            query = query.filter((Q(User=request.user) & Q(Sold_unsold='ON_CART')) | Q(Sold_unsold='UNSOLD'))
                            product_list = query.order_by('-id').all()
                    
                    data = ProductSerializer(product_list, many=True).data
                    cart_obj = Cart.objects.new_or_get(request)
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
                    if cart_obj.products.filter(pk=product_obj.pk).exists():
                        returnData = {
                            'state': "FAIL",
                            'error': "This item has already added to cart."
                        }
                        return JsonResponse(returnData)
                    else:
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

                check_status = checker_api(product_id, checker_id, request.user.id)
                check_status = check_status[:-1]
                print(check_status)
                if check_status == 'Done':
                    returnData = {
                        'state': check_status,
                    }
                    cart_obj.products.remove(product_obj)
                elif check_status == 'Fail':
                    returnData = {
                        'state': check_status,
                        'error': "This is Invalid Phone. This item price has been refuned to your balance."
                    }
                    cart_obj.products.remove(product_obj)
                else:
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
                query = Order_history.objects.filter(Checker_status='Done').order_by('-id').all()
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


def checker_api(product_id, checker_id, user_id):
    checker_name = Checker.objects.get(id=checker_id).Name + '.py'
    commend = 'python3 %s %d %d %d' % (checker_name, product_id, checker_id, user_id)
    os.system(commend + ' > tmp')
    result = open('tmp', 'r').read()
    os.remove('tmp')
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
                for row in range(batch_num):
                    batch_list = request.POST.getlist(f'batch_list[{row}][]')
                    row_dic = {}
                    for i in range(len(field_list)):
                        print(repr(row_dic))
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

                    row_dic_keys = row_dic.keys()
                    if 'Gender' in row_dic_keys:
                        if row_dic['Gender'] == 'Male':
                            row_dic['Gender'] = 'M'
                        elif row_dic['Gender'] == 'Female':
                            row_dic['Gender'] = 'F'
                        else:
                            row_dic['Gender'] = 'U'
                    if 'Exp_day' in row_dic_keys:
                        row_dic['Exp_day'] = int(row_dic['Exp_day'])
                    if 'Exp_month' in row_dic_keys:
                        row_dic['Exp_month'] = int(row_dic['Exp_month'])
                    if 'Exp_year' in row_dic_keys:
                        row_dic['Exp_year'] = int(row_dic['Exp_year'])
                    data.append(row_dic)

                many = isinstance(data, list)
                serializer = ShopDataSerializer(data=data, many=many)
                
                if serializer.is_valid(raise_exception=True):
                    serializer.save()                
                    returnData = {
                        'state': "OK",
                        'data': data
                    }
                else:
                    returnData = {
                        'state': "FAIL",
                        'error': serializer.errors
                    }
            except Exception as e:
                if(new_batch):
                    new_batch.delete()
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
        product_query = Shop_data.objects.order_by('Insert_date')
        if product_query.exists():
            start_date = product_query.first().Insert_date.strftime('%m/%d/%Y')
            end_date = product_query.last().Insert_date.strftime('%m/%d/%Y')
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
                    products = Shop_data.objects.filter(Batch=batch).filter(Supplier_payment_status=PaidUnpaid).filter(Sold_date__date__range=(from_date, to_date))
                    sold_products = products.filter(Sold_unsold='SOLD')
                    refund_products = products.filter(Sold_unsold='REFUND')
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
            products = Shop_data.objects.filter(Batch=batch_obj).filter(Supplier_payment_status=PaidUnpaid).filter(Sold_date__date__range=(from_date, to_date))
            if get_type == 'total-sold':
                sold_products = products.filter(Sold_unsold='SOLD')
                query = sold_products
            elif get_type == 'total-refund':
                refund_products = products.filter(Sold_unsold='REFUND')
                query = refund_products
            elif get_type == 'total-unsold':
                unsold_products = products.filter(Q(Sold_unsold='ON_CART') | Q(Sold_unsold='UNSOLD'))
                query = unsold_products
            data = RecordsSerializer(query, many=True).data
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