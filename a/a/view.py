# -*- coding:utf-8 -*-
from django.http import HttpResponse
import json
from django.http import JsonResponse


def hello(request):
    var1 = request.GET['var1']
    var2 = request.GET['var2']
    # return HttpResponse('{var1} {var2}'.format(var1=var1, var2=var2))
    return HttpResponse('{var}'.format(var=request.body.decode('utf-8')))

def _get_response_json_dict(data, err_code=0, message='Success'):
    ret = {
        'err_code':err_code,
        'message':message,
        'data':data
    }
    return ret

def get_sum(request):
    received_data = json.loads(request.body)
    var1 = received_data['var1']
    var2 = received_data['var2']

    sum =var1+var2
    response_data = {'sum':sum}
    return JsonResponse(_get_response_json_dict(data=response_data))

