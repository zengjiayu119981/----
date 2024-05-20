from django.shortcuts import render,redirect
from django.http import JsonResponse
from django import forms
from api import models
from api.utils.token import create_token
from django.forms.models import model_to_dict
import time,math,requests
from django.core.files.storage import default_storage
from django.db.models import F

# Create your views here.
#user ModelForm
class UserInfoModelForm(forms.ModelForm):
    username = forms.CharField(max_length=11)

    class Meta:
        model = models.userInfo   # 与models建立了依赖关系
        fields = ['password']


#用户登录
def user_login(request):
    #post请求
    if request.method == 'POST':
        obj = UserInfoModelForm(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data["username"]
            password = obj.cleaned_data["password"]
            user_obj = models.userInfo.objects.filter(password=password,username=username).first()
            if user_obj:
                print("用户",username,"登陆成功")
                token = create_token(username,"user")
                return JsonResponse({'msg':'login_success','name':username,'token':token,'type':'user'})
            else :
                print("登录失败")
                return JsonResponse({'msg':"用户名不存在或密码错误"})
        else :
            return JsonResponse({'msg':'格式错误'})
    #重定位至登录界面
    return redirect("/login/")



#用户注册
def register(request):
    if request.method == 'POST':
        obj = UserInfoModelForm(request.POST) 
        print(obj.errors.as_text())
        print(obj.data)
        if obj.is_valid():
            username = obj.cleaned_data["username"]
            password = obj.cleaned_data["password"]
            user_obj = models.userInfo.objects.filter(username=username).first()
            if user_obj:
                print("用户",username,"用户名存在")
                return JsonResponse({'msg':'用户名存在'})
            else :
                models.userInfo.objects.create(username=username,password=password,create_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
                token = create_token(username,"user")
                print("注册成功  用户名",username)
                return JsonResponse({'msg':"register_success",'name':username,'token':token,'type':'user'})
        else :
            return JsonResponse({'msg':''})
    #重定位至登录界面
    return redirect("/login/")


def get_user_posts(request):
    username = request.GET.get('username')
    currentpage = request.GET.get('currentpage')
    currentpage = int(currentpage)
    posts_list = models.post.objects.filter(user=username).order_by('-create_time')
    data=[]
    start_item = (currentpage-1)*10
    end_item = currentpage*10
    if end_item > posts_list.count():
        end_item = posts_list.count()
    for i in range(start_item,end_item):
        d = model_to_dict(posts_list[i])
        d["content"] = posts_list[i].content[:30]
        d['image'] = default_storage.url(d['image'])
        d['image'] = request.build_absolute_uri(d['image'])
        data.append(d)
    print(data)
    print("返回帖子列表",data)
    page_data={
        "total":posts_list.count(),
        "data":data
    }
    return JsonResponse(page_data, safe=False)
        
def user_post_delete(request):
    post_id = request.POST.get("post_id")
    username = request.META.get('HTTP_USERNAME')
    post = models.post.objects.filter(user=username,post_id=post_id)
    post.delete()
    posts_list = models.post.objects.filter(user=username).order_by('-create_time')
    data=[]
    start_item = 0
    end_item = 10
    if end_item > posts_list.count():
        end_item = posts_list.count()
    for i in range(start_item,end_item):
        d = model_to_dict(posts_list[i])
        d["content"] = posts_list[i].content[:30]
        d['image'] = default_storage.url(d['image'])
        d['image'] = request.build_absolute_uri(d['image'])
        data.append(d)
    print(data)
    print("返回帖子列表",data)
    page_data={
        "total":posts_list.count(),
        "data":data
    }
    return JsonResponse(page_data, safe=False)


def get_user_comments(request):
    username = request.GET.get('username')
    currentpage = request.GET.get('currentpage')
    currentpage = int(currentpage)
    posts_list = models.comment.objects.filter(user=username).annotate(post_title = F('post_id__title')).order_by('-create_time')
    print(posts_list[1].post_title)
    data=[]
    start_item = (currentpage-1)*10
    end_item = currentpage*10
    if end_item > posts_list.count():
        end_item = posts_list.count()
    for i in range(start_item,end_item):
        d = model_to_dict(posts_list[i])
        d["content"] = posts_list[i].content[:30]
        d["post_title"]=posts_list[i].post_title
        data.append(d)
    print(data)
    print("返回帖子列表",data)
    page_data={
        "total":posts_list.count(),
        "data":data
    }
    return JsonResponse(page_data, safe=False)


def user_comment_delete(request):
    comment_id = request.POST.get("comment_id")
    username = request.META.get('HTTP_USERNAME')
    comment = models.comment.objects.filter(user=username,comment_id=comment_id)
    comment.delete()
    posts_list = models.comment.objects.filter(user=username).annotate(post_title = F('post_id__title')).order_by('-create_time')
    print(posts_list[1].post_title)
    data=[]
    start_item = 0
    end_item = 10
    if end_item > posts_list.count():
        end_item = posts_list.count()
    for i in range(start_item,end_item):
        d = model_to_dict(posts_list[i])
        d["content"] = posts_list[i].content[:30]
        d["post_title"]=posts_list[i].post_title
        data.append(d)
    page_data={
        "total":posts_list.count(),
        "data":data
    }
    return JsonResponse(page_data, safe=False)


def user_info(request):
    username = request.META.get('HTTP_USERNAME')
    user_obj = models.userInfo.objects.filter(username=username).first()
    user_info = model_to_dict(user_obj)
    return JsonResponse(user_info,safe=False)


def user_info_update(request):
    username = request.META.get('HTTP_USERNAME')
    gender = request.POST.get('gender')
    signature = request.POST.get('signature')
    user_obj = models.userInfo.objects.filter(username=username).first()
    user_obj.gender = gender
    user_obj.signature = signature
    user_obj.save()
    user_info = model_to_dict(user_obj)
    return JsonResponse({"data":user_info,"msg":'更新成功'},safe=False)