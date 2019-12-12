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
     url(r'^customer/add/', AddOrEdit.as_view(),name="customer_add"),
     # url(r'^customer/add/', CustomerEditOrAdd.as_view(),name="customer_add"),
    #编辑
     url(r'^customer/edit/(-*\d+)/', AddOrEdit.as_view(),name="customer_edit"),
     # url(r'^customer/edit/(-*\d+)/', CustomerEditOrAdd.as_view(),name="customer_edit"),
     # url(r'^customer/edit/(\d+)/', CustomerEditOrAdd.as_view(),name="customer_edit"),
     #删除
     url(r'^customer/del/(-*\d+)/', CustomerDel,name="customer_del"),
    #跟进记录
     url(r'^consult_recode/list/', ConsultRecode.as_view(),name="consult_recode"),
    #编辑及添加跟进记录
     url(r'^consult_recode/edit/(-*\d+)/', AddOrEdit.as_view(),name="consult_recode_edit"),
     # url(r'^consult_recode/edit/(-*\d+)/', ConsultRecodeEditOrAdd.as_view(),name="consult_recode_edit"),
     # url(r'^consult_recode/add/', ConsultRecodeEditOrAdd.as_view(),name="consult_recode_add"),
     url(r'^consult_recode/add/', AddOrEdit.as_view(),name="consult_recode_add"),
    #删除
     url(r'^consult_recode/del/(-*\d+)/', ConsultRecodeDel,name="consult_recode_del"),


#跟进记录
     url(r'^enrollment/list/', EnrollMent.as_view(),name="enrollment"),
    #编辑及添加跟进记录
     url(r'^enrollment/edit/(-*\d+)/', AddOrEdit.as_view(),name="enrollment_edit"),
     # url(r'^enrollment/edit/(-*\d+)/', EnrollMentEditOrAdd.as_view(),name="enrollment_edit"),
     # url(r'^enrollment/add/', EnrollMentEditOrAdd.as_view(),name="enrollment_add"),
     url(r'^enrollment/add/', AddOrEdit.as_view(),name="enrollment_add"),
    #删除
     url(r'^enrollment/del/(-*\d+)/', EnrollMentDel,name="enrollment_del"),
    # 错误页面
     url(r'.*', error,name="error"),
]