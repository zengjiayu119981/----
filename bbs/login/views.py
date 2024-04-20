from django.shortcuts import render,redirect
from django.http import JsonResponse
from django import forms
from django.forms import fields
from login import models

# # Create your views here.
# #user ModelForm
# class UserInfoModelForm(forms.ModelForm):

#     class Meta:
#         model = models.userInfo   # 与models建立了依赖关系
#         fields = ['username','password']




# #用户登录
# def user_login(request):
#     #post请求
#     if request.method == 'POST':
#         obj = UserInfoModelForm(request.POST)
#         if obj.is_valid():
#             username = obj.cleaned_data["username"]
#             password = obj.cleaned_data["password"]
#             user_obj = models.userInfo.objects.filter(password=password,username=username).first()
#             if user_obj:
#                 print("用户",username,"登陆成功")
#                 return JsonResponse({'msg':'login_success'})
#             else :
#                 print("登录失败")
#                 return JsonResponse({'msg':"用户名不存在或密码错误"})
#         else :
#             return JsonResponse({'msg':''})
#     #重定位至登录界面
#     return redirect("/login/")


# #管理员登陆
# def manager_login():
#     pass