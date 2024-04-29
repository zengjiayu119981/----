import api.models as models
import os
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from api.models import post
from django import forms
import requests

class PostModelForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title', 'content', 'plate', 'user']
        


def get_posts_list(request):

    title = request.POST.get('title')
    posts_list = models.post.objects.filter(plate_id=title)
    data=[]
    for plate in posts_list:
        d = model_to_dict(plate)
        d["content"] = plate.content[:50]
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

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('image'):
        file = request.FILES['image']
        
        # 如果使用模型存储
        # uploaded_file = UploadedFile(file=file)
        # uploaded_file.save()
        # file_url = request.build_absolute_uri(uploaded_file.file.url)
        
        # 或者直接处理，例如保存到特定目录
        file_path = os.path.join('uploads/', file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        file_url = request.build_absolute_uri('/media/' + file.name)  # 假设MEDIA_URL设置为'/media/'
        
        return JsonResponse({'url': file_url})
    else:
        return JsonResponse({'error': 'No file uploaded or invalid request method.'}, status=400)
    


def create_post(request):
    if request.method == 'POST':
        # 假设前端发送的数据结构与下面一致
        response_data = {}
        obj = PostModelForm(request.POST) 
        
        print(request.POST)
        if obj.is_valid():
            title = obj.cleaned_data['title']
            content = obj.cleaned_data['content']
            response_data = requests.post(url="http://127.0.0.1:9102/comment/moderation",json={"comments":[content],'mode':'fast'})
            if response_data.status_code == 200:
                response_data = response_data.json()
                moderation_result = 0
                print(response_data['results'])
                for coment,result in response_data.get('results').items():
                    print(coment,"  label : ",result['label'])
                    if result['label'] == 1:
                        moderation_result = 1
                        break

                if moderation_result == 0:
                    obj.save()
                    response_data = {
                        'message': f"Received post with title: '{title}' and content: '{content}'",
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