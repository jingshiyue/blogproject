from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from . views import hash_code
myUser = get_user_model()    #等同于Userprofile

class MyCustomBackend(ModelBackend):  
    def authenticate(self,request,username=None, password=None, **kwargs):  #一定要有request参数，不然不会进入该函数体内
        try:
            user = myUser.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username)) #用户名、邮箱、手机、都能登录
            print("auth.py.user",user)
            print(password)
            if user.check_password(password):  #自带加密认证 ，如登陆页面认证超级管理员
                return user
            if user.password == hash_code(password): #自定义加密认证
                return user
        except Exception as e:
            return None
   
    # def get_user(self, user_id):  
    #     try:  
    #         myUser.objects.get(pk=id)
    #         return myUser.objects.get(pk=id)
    #     except myUser.DoesNotExist:  
    #         return None
        