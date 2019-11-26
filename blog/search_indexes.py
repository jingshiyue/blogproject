#!/usr/bin/python3
# Time : 2019/11/26 11:42 
# Author : zcl
from haystack import indexes
from .models import Post
"""
要相对某个 app 下的数据进行全文检索，就要在该 app 下创建一个 search_indexes.py 文件，
然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Post），并且继承 SearchIndex 和 Indexable。
"""

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #每个索引里面必须有且只能有一个字段为 document=True,一般约定此字段名为text
                                                                #use_template,使用数据模板去建立搜索引擎索引的文件
    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()