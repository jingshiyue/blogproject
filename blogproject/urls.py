"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from blog.feeds import AllPostsRssFeed
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^comments', include('comments.urls')),
    url(r'^login/', include('login.urls')),
    url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),   
    url(r'^search/', include('haystack.urls')),  #搜索的视图函数和 URL 模式 django haystack 都已经帮我们写好了，只需要项目的 urls.py 中包含它：
    url(r'^about/',views.about,name='about'),
    url(r'^contact/',views.contact,name='contact'),
]


