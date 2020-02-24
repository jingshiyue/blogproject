from django.apps import AppConfig


class LoginConfig(AppConfig):
    name = 'login'



# class UsersConfig(AppConfig):
#     name = 'users'
#     #app名字后台显示中文
#     verbose_name = "用户管理"  #配置在后台中的左侧列表里的中文别名，还需在__init__中配置

#     def ready(self):   #复写AppConfig的函数，该函数会在django启动时被运行
#         import users.signals