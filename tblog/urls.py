from django.conf.urls import url
from django.contrib import admin
from tblog import views
from django.views.static import serve
from Myblog import settings


from tblog import views

urlpatterns = [
    url(r'^updown/',views.updown),
    # 个人站点页面
    url(r'^(?P<username>\w+)/$', views.home_site),
    # 归档
    url(r'^(?P<username>\w+)/(?P<condition>cate|tag|date)/(?P<param>.*)', views.home_site),
    # 文章详细页
    url(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)', views.article_detail),




]