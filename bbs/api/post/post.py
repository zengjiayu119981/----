import api.models as models
import os
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from api.models import post
from django import forms
import requests
from django.core.files.storage import default_storage
import math

class PostModelForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = post
        fields = ['title', 'content', 'plate', 'user','image']


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = models.comment
        fields = ['post', 'user', 'content']     


def get_posts_list(request):

    title = request.POST.get('title')
    posts_list = models.post.objects.filter(plate_id=title)
    data=[]
    for post in posts_list:
        d = model_to_dict(post)
        d["content"] = post.content[:50]
        d['image'] = default_storage.url(d['image'])
        d['image'] = request.build_absolute_uri(d['image'])
        data.append(d)
    print(data)
    print("返回帖子列表",data)
    page_data={
        "page_num":posts_list.count(),
        "data":data
    }
    return JsonResponse(page_data, safe=False)

def get_post_detail(request):
    post_id = request.POST.get('post_id')
    print(post_id)
    post = models.post.objects.filter(post_id=post_id)
    data = model_to_dict(post[0])
    data['image'] = default_storage.url(data['image'])
    data['image'] = request.build_absolute_uri(data['image'])
    print("返回帖子详情",data)
    return JsonResponse(data, safe=False)
    

def create_post(request):
    if request.method == 'POST':
        # 假设前端发送的数据结构与下面一致
        response_data = {}
        obj = PostModelForm(request.POST,request.FILES) 
        
        print(request.POST)
        if obj.is_valid():
            title = obj.cleaned_data['title']
            content = obj.cleaned_data['content']
            print(obj.cleaned_data["image"])
            response_data = requests.post(url="http://localhost:9102/comment/moderation",json={"comments":[content],'mode':'fast'})
            if response_data.status_code == 200:
                response_data = response_data.json()
                moderation_result = 0
                for coment,result in response_data.get('results').items():
                    print(coment,"  label : ",result['label'])
                    if result['label'] == 1:
                        moderation_result = 1
                        break

                if moderation_result == 0:
                    obj.save()
                    response_data = {
                        'message': f"发布成功",
                        'received_at': timezone.now().isoformat(),
                    }
                    

                else:
                    response_data = {
                        'message': f"你的言论有不良信息",
                        'received_at': timezone.now().isoformat(),
                    }
            else:
                response_data = {
                    'message': f"未成功发布",
                    'received_at': timezone.now().isoformat(),
                }
        else:
            for field, errors in obj.errors.items():
                print(f"字段 '{field}' 验证失败，原因：")
                for error in errors:
                    print(f"- {error}") 
        return JsonResponse(response_data, status=201)
                 
    else:

        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def get_comments(request):
    post_id = request.POST.get('post_id')
    page = request.POST.get('page')
    comments = models.comment.objects.filter(post_id=post_id).order_by('-create_time')
    num = comments.count()
    # start = (page-1)*10
    # end = page*10
    # if end>num:
    #     end = num
    data=[]
    # for i in range(start,end):
    #     d = model_to_dict(comments[i])
    #     data.append(d)
    for comment in comments:
        d = model_to_dict(comment)
        d["create_time"] = comment.create_time.astimezone(timezone.utc).isoformat()
        print(d)
        data.append(d)
    print("post_id:",post_id,"    comments:\n",data)
    return JsonResponse({"data":data,"page_num":num/10.0}, safe=False)


def create_comment(request):
    if request.method == 'POST':
        # 假设前端发送的数据结构与下面一致
        response_data = {}
        obj = CommentModelForm(request.POST,request.FILES) 
        
        print(request.POST)
        if obj.is_valid():
            content = obj.cleaned_data['content']
            response_data = requests.post(url="http://localhost:9102/comment/moderation",json={"comments":[content],'mode':'fast'})
            if response_data.status_code == 200:
                response_data = response_data.json()
                moderation_result = 0
                for coment,result in response_data.get('results').items():
                    print(coment,"  label : ",result['label'])
                    if result['label'] == 1:
                        moderation_result = 1
                        break

                if moderation_result == 0:
                    obj.save()
                    response_data = {
                        'message': f"发布成功",
                        'received_at': timezone.now().isoformat(),
                    }
                    

                else:
                    response_data = {
                        'message': f"你的言论有不良信息",
                        'received_at': timezone.now().isoformat(),
                    }
            else:
                response_data = {
                    'message': f"未成功发布",
                    'received_at': timezone.now().isoformat(),
                }
        else:
            for field, errors in obj.errors.items():
                print(f"字段 '{field}' 验证失败，原因：")
                for error in errors:
                    print(f"- {error}") 

        print(timezone.now())
        return JsonResponse(response_data, status=201)
                 
    else:

        return JsonResponse({"error": "Invalid request method"}, status=405)