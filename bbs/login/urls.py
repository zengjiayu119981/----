from django.urls import path
from django.views.generic.base import TemplateView

app_name = 'login'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [ 
    path('', TemplateView.as_view(template_name='login/index.html')),
]