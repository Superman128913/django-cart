from logging import exception
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import F, Q, Count

from apps.home.views import get_default_page_context
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
                if object == 'batch':
                    batch_list = request.POST.getlist('batch_list[]')
                    batch_list = list(map(int, batch_list))
                    query = Shop_data.objects.filter(Batch__in=batch_list).values('Areaf1').distinct().all()
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
                    query = Shop_data.objects.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).values('Areaf2').distinct().all()
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
                    query = Shop_data.objects.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).values('Areaf3').distinct().all()
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
                    query = Shop_data.objects.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).values('Areaf4').distinct().all()
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
                    query = Shop_data.objects.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).values('Areaf5').distinct().all()
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
                    query = Shop_data.objects.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).filter(Areaf5__in=areaf5_list).values('State').distinct().all()
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
                    query = Shop_data.objects.filter(Batch__in=batch_list).filter(Areaf1__in=areaf1_list).filter(Areaf2__in=areaf2_list).filter(Areaf3__in=areaf3_list).filter(Areaf4__in=areaf4_list).filter(Areaf5__in=areaf5_list).filter(State__in=state_list).values('City').distinct().all()
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
            batch_list = request.POST.getlist('batch_list[]')
            if len(batch_list):
                query = Shop_data.objects.filter(Batch__in=batch_list)

                gender_list = request.POST.getlist('gender_list[]')
                if len(gender_list):
                    query = query.filter(Gender__in=gender_list)

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
                        
                    area_code_list = request.POST.getlist('area_code_list[]')
                    if len(area_code_list):
                        print(area_code_list)
                        query = query.filter(Area_code__in=area_code_list)
                    else:
                        zipcode_list = request.POST.getlist('zipcode_list[]')                        
                        if len(zipcode_list):
                            print(zipcode_list)
                            query = query.filter(Zipcode__in=zipcode_list)
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
                            elif len(state_list):
                                query = query.filter(State__in=state_list)
                            elif len(areaf5_list):
                                query = query.filter(Areaf5__in=areaf5_list)
                            elif len(areaf4_list):
                                query = query.filter(Areaf4__in=areaf4_list)
                            elif len(areaf3_list):
                                query = query.filter(Areaf3__in=areaf3_list)
                            elif len(areaf2_list):
                                query = query.filter(Areaf2__in=areaf2_list)
                            elif len(areaf1_list):
                                query = query.filter(Areaf1__in=areaf1_list)

                    product_list = query.all()
                    data = ProductSerializer(product_list, many=True).data
                    returnData = {
                        'state': 'OK',
                        'data': data
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