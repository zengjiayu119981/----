import api.models as models
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict


def get_plate_list(request):
    plates_list = models.plate.objects.all()
    print(plates_list)
    data=[]
    for plate in plates_list:
        d = model_to_dict(plate,exclude=["pic"])
        data.append(d)
    print("返回板块列表",data)
    return JsonResponse(data, safe=False)