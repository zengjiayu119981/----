from django.urls import path
from django.views.generic.base import TemplateView
from api.user.user import user_login,register,get_user_posts
from api.plate.plate import get_plate_list
from api.post.post import get_posts_list,get_post_detail,create_post,get_comments,create_comment


app_name = 'api'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [ 
    path('login/user', user_login),
    path('register/user', register),
    path('plate/list', get_plate_list),
    path('posts/list',get_posts_list),
    path('post/detail',get_post_detail),
    path('public/post',create_post),
    path("comments",get_comments),
    path('publish/comment',create_comment),
    path('user/posts',get_user_posts)
]