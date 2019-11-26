#!/usr/bin/python3
# Time : 2019/11/14 17:41 
# Author : zcl
"""
自定义模板标签
"""
from ..models import Post,Category
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    """
    这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，并将函数 get_recent_posts 装饰为 register.simple_tag。这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了。
    """
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

# @register.simple_tag
# def get_categories():
#     # 别忘了在顶部引入 Category 类
#     return Category.objects.all()
@register.simple_tag
def get_categories():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
