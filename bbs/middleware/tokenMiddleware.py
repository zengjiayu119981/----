from api.utils.token import check_token
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin



API_USER = ["/api/post"]

class tokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path  in API_USER:
          # 从请求头中获取 username 和 token
          username = request.META.get('HTTP_USERNAME')
          token = request.META.get('HTTP_AUTHORIZATION')
          print("username:  ",username)
          if username is None or token is None:
              return JsonResponse({'errno': 100001, 'msg': "未查询到登录信息"})
          else:
              # 调用 check_token 函数验证
              if check_token(username, token):
                  return None
              else:
                  return JsonResponse({'errno': 100002, 
                                       'msg': "登录信息错误或已过期"})
        return None
              