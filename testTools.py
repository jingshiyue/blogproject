import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogproject.settings")
import django
django.setup()

from blog.models import *
post_list = Post.objects.all().order_by("-id","author_id")

print(post_list)
print(len(post_list))


post = Post.objects.all().get(title="冬天").body
post = Post.objects.all().filter(title="冬天").values("body")
print(post)
print(post_list)

category = Post.objects.all().get(title="冬天").category
print(category)

author =  Post.objects.all().get(title="冬天").author
print(author)

posts = Category.objects.all().get(id=1).post_set.all() #没有related_name时用，有related_name会报错
print(posts)

posts = Category.objects.all().get(id=1).related_name.all() #related_name='category_name'
print(posts)




post_list = Post.objects.all().filter(id__gte=4)
posts1 = Post.objects.all().filter(category__name="风景") #正向查询，由Post里的category外键查到Category表，再查表里name字段
print(posts1)
Category1 = Category.objects.all().filter(post__title='冬天') #反向查询，没有related_name
print(Category1)
Category2 = Category.objects.all().filter(related_name__title='冬天') #反向查询,有related_name
print(Category2)
print("=========================")

