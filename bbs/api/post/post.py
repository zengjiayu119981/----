import api.models as models
import os
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from api.models import post


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
        obj = post(request.POST) 
        data = request.POST
        title = data.get('title')
        content = data.get('content')
        # 注意：这里没有处理文件上传，如果需要处理文件，请参考前面关于文件上传的回答  
        # 示例：简单地记录接收到的数据
        # 实际应用中，你可能会将这些数据保存到数据库或其他存储中
        response_data = {
            'message': f"Received post with title: '{title}' and content: '{content}'",
            'received_at': timezone.now().isoformat(),
        }
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)