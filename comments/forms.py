#!/usr/bin/python3
# Time : 2019/11/15 11:15 
# Author : zcl

from django import forms
from .models import Comment

#对comment里的model 里 封装成表单类型
class CommentForm(forms.ModelForm): #通过调用这个类forms.ModelForm的一些方法和属性，Django 将自动为我们创建常规的表单代码
    class Meta: #内部类 Meta
        model = Comment #规则：model = Comment 表明这个表单对应的数据库模型是 Comment 类
        fields = ['name', 'email', 'url', 'text'] #规则：指定了表单需要显示的字段
