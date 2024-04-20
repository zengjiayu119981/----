import api.models as models
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict


def get_posts_list(request):

    title = request.POST.get('title')
    posts_list = models.post.objects.filter(plate_id=title)
    data=[]
    for plate in posts_list:
        d = model_to_dict(plate)
        d["content"] = plate.content[:20]
        data.append(d)
    print(data)
    print("返回帖子列表",data)
    return JsonResponse(data, safe=False)

def get_post_detail(request):
    post_id = request.POST.get('post_id')
    print(post_id)
    post = models.post.objects.filter(post_id=post_id)
    data = model_to_dict(post[0])
    print("返回帖子详情",data)
    return JsonResponse(data, safe=False)
    