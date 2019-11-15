#!/usr/bin/python3
# Time : 2019/11/15 11:36 
# Author : zcl
from django.conf.urls import url
from . import views

app_name = 'comments' #这个很重要，命名区别
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]