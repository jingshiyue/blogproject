import os,sys
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogproject.settings")
import django
django.setup()

from blog.models import *

post_list = Post.objects.all()
print(post_list)