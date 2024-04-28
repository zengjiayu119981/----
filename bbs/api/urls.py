from django.urls import path
from django.views.generic.base import TemplateView
from api.user.user import user_login,register
from api.plate.plate import get_plate_list
from api.post.post import get_posts_list,get_post_detail,upload_file,create_post
from django.conf import settings
from django.conf.urls.static import static


app_name = 'api'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [ 
    path('login/user', user_login),
    path('register/user', register),
    path('plate/list', get_plate_list),
    path('posts/list',get_posts_list),
    path('post/detail',get_post_detail),
    path('public/post',create_post),
    path('upload',upload_file)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)