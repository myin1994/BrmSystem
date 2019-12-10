from django.conf.urls import url
from app01.views import *
urlpatterns = [
    url(r'^login/', Login.as_view(),name="login"),
    url(r'^logout/', Logout.as_view(),name="logout"),
    url(r'^register/', Register.as_view(),name="register"),
    #首页
    url(r'^home/', Home.as_view(),name="home"),
    #公户管理&我的客户
     url(r'^customers/', Customers.as_view(),name="customers"),
     url(r'^mycustomers/', Customers.as_view(),name="mycustomers"),
    #添加
     url(r'^customer/add', CustomerEditOrAdd.as_view(),name="customer_add"),
    #编辑
     url(r'^customer/edit/(-*\d+)/', CustomerEditOrAdd.as_view(),name="customer_edit"),
     # url(r'^customer/edit/(\d+)/', CustomerEditOrAdd.as_view(),name="customer_edit"),
     #删除
     url(r'^customer/del/(-*\d+)/', CustomerDel,name="customer_del"),
     url(r'.*', error,name="error"),
]