from django.db import models
# Create your models here.

# 用户表
class userInfo(models.Model):


    #性别选项
    gender_choices = (
        (0,"女"),
        (1,"男")
    )



    #用户名
    username = models.CharField(max_length=32, verbose_name="用户名",primary_key=True)

    #密码
    password = models.CharField(max_length=64, verbose_name="密码")

    #性别
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name="性别" ,null=True)

    #注册时间
    create_time = models.DateTimeField(verbose_name="建立时间", null=True)

    #发帖数
    TotalPosts = models.IntegerField(verbose_name="发帖数", null=True)

    #签名
    signature = models.TextField(verbose_name="签名", null=True)

    def __str__(self) -> str:
        return self.username
    


#板块
class plate(models.Model):



    #标题
    title = models.CharField(max_length=100,unique=True,primary_key=True)

    #创建时间
    create_time = models.DateTimeField()

    #图片
    pic = models.ImageField(upload_to='plate/pic/',verbose_name="图片",null=True)

    def __str__(self) -> str:
        return self.title
    



#帖子
class post(models.Model):

    #帖子id
    post_id = models.AutoField(primary_key=True)

    #标题
    title = models.TextField()

    #用户id
    user = models.ForeignKey(userInfo, on_delete = models.SET_NULL,to_field='username', null=True)

    #论坛id
    plate = models.ForeignKey(plate, on_delete = models.SET_NULL,to_field='title', null=True)

    #创建时间
    create_time = models.DateTimeField(null=True,auto_now_add=True)

    #内容
    content = models.TextField()

    image = models.ImageField(upload_to='post/pic/',verbose_name="图片",null=True, blank=True)

    def __str__(self) -> str:
        return self.title

class comment(models.Model):
    #评论id
    comment_id = models.AutoField(primary_key=True)
    #帖子id
    post = models.ForeignKey(post, on_delete=models.CASCADE,to_field='post_id')
    #用户id
    user = models.ForeignKey(userInfo, on_delete=models.CASCADE,to_field='username')
    #评论内容
    content = models.TextField()
    #评论时间
    create_time = models.DateTimeField(auto_now_add=True)