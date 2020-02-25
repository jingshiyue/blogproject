from django.test import TestCase

# Create your tests here.
# import datetime
# from django.utils import timezone
from django.test import TestCase
# from django.db import models
from . models import *

"""
1、用自己单独的数据库，不能查出项目里的数据；
2、只能对同app内的models测试？能跨app测试吗？
3、直接python manage.py test app 运行，不用启动项目(runserver)才能进行测试；
"""
class ormTests(TestCase):
    def test_orm(self):
        """
        在将来发布的问卷应该返回False
        """

        # time = timezone.now() + datetime.timedelta(days=30)
        # future_question = Question(pub_date=time)
        # self.assertIs(future_question.was_published_recently(), False)
        post_list = Post.objects.all()   #QuerySet类型
        print(post_list)
        print(type(post_list))