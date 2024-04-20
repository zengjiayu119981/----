from django.shortcuts import render,redirect
from django.http import JsonResponse
from django import forms
from api import models
from api.utils.token import create_token
import time
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
