import time
from django.core import signing
import hashlib

HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = "Zewan"
SALT = "blog.zewan.cc"

def encrypt(obj):
  """加密：signing 加密 and Base64 编码"""
  value = signing.dumps(obj, key=KEY, salt=SALT)
  value = signing.b64_encode(value.encode()).decode()
  return value

def decrypt(src):
  """解密：Base64 解码 and signing 解密"""
  src = signing.b64_decode(src.encode()).decode()
  raw = signing.loads(src, key=KEY, salt=SALT)
  return raw

def create_token(name,typ):
  """生成token信息"""
  # 1. 加密头信息
  header = encrypt(HEADER)
  # 2. 构造Payload(有效期14天)
  payload = {"name": name, "iat": time.time(), 
             "exp": time.time()+1209600.0,'type':typ}
  payload = encrypt(payload)
  # 3. MD5 生成签名
  md5 = hashlib.md5()
  md5.update(("%s.%s" % (header, payload)).encode())
  signature = md5.hexdigest()
  token = "%s.%s.%s" % (header, payload, signature)
  return token

def get_payload(token):
  """解析 token 获取 payload 数据"""
  payload = str(token).split('.')[1]
  payload = decrypt(payload)
  return payload

def get_username(token):
  """解析 token 获取 name"""
  payload = get_payload(token)
  return payload['name']

def get_typ(token):
  """解析 token 获取类型"""
  payload = get_payload(token)
  return payload['type']

def get_exp_time(token):
  """解析 token 获取过期时间"""
  payload = get_payload(token)
  return payload['exp']

def check_token(name, token):
  """验证 token：检查 username 和 token 是否一致且未过期"""
  return get_username(token) == name and get_exp_time(token) > time.time() and get_typ(token)=='user'

def manager_check_token(name,token,typ):
  """验证 token：检查 username 和 token 是否一致且未过期"""
  return get_username(token) == name and get_exp_time(token) > time.time() and get_typ(token)=='manafer'