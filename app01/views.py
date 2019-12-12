from django.shortcuts import render, redirect, HttpResponse
from django.http import *
from django.views import View
from django.utils.decorators import method_decorator
from django.urls import reverse
from app01 import models
from django.db import transaction
from django.db.models import *
from django.db.utils import *
# Create your views here.
from app01.app01forms import *


def error(request):
    return render(request, "error.html")


class Login(View):
    def get(self, request):
        obj = UserLoginForm()
        return render(request, 'auth/login.html', locals())

    def post(self, request):
        obj = UserLoginForm(request.POST)
        if obj.is_valid():
            request.session["status"] = "success"
            request.session["username"] = request.POST.get("username")
            request.session["userid"] = models.UserInfo.objects.get(username=request.POST.get("username")).id
            return redirect('app01:home')
        else:
            return render(request, 'auth/login.html', locals())


class Logout(View):
    """
    注销
    """

    def get(self, request):
        request.session.flush()
        return redirect('app01:login')


class Register(View):

    def get(self, request):
        obj = UserForm()
        return render(request, 'auth/register.html', locals())

    def post(self, request):
        obj = UserForm(request.POST)
        if obj.is_valid():
            data = obj.cleaned_data
            data.pop("confirm_password")
            models.UserInfo.objects.create(**data)
            return redirect('app01:login')
        else:
            return render(request, 'auth/register.html', locals())


class Home(View):
    def get(self, request):
        return render(request, 'home.html')


from utils.Pagination import Paginaton


class Customers(View):
    def search(self, search_model, search_value, search_path, search_uesr):

        if search_model and search_value:
            if search_path == reverse('app01:mycustomers'):
                all_customers = models.Customer.objects.filter(is_delete=False, consultant__id=search_uesr,
                                                               **{search_model: search_value})
            else:
                all_customers = models.Customer.objects.filter(is_delete=False, consultant__isnull=True,
                                                               **{search_model: search_value})
        else:
            if search_path == reverse('app01:mycustomers'):
                all_customers = models.Customer.objects.filter(is_delete=False, consultant__id=search_uesr)
            else:
                all_customers = models.Customer.objects.filter(is_delete=False, consultant__isnull=True)
        return all_customers.order_by('-date')

    def get(self, request, msg=""):
        search_model = request.GET.get('search_model')  # 查询模式
        search_value = request.GET.get('search_value')  # 查询关键字
        search_uesr = request.session.get('userid')  # 查询者id
        all_customers = self.search(search_model, search_value, request.path, search_uesr)
        # 获取页数
        current_page = request.GET.get('page')
        # 计算查询对象总量
        total_count = all_customers.count()
        # 获取get请求数据
        get_data = request.GET
        # 实例化分页对象并传入相关数据
        page_obj = Paginaton(current_page, total_count, get_data)
        # 获取一页显示的数据对象
        all_customers_filter = all_customers[page_obj.start:page_obj.end]
        # 获取分页组件html
        page_html = page_obj.page_html()
        return render(request, 'sales/customer_list.html', locals())

    def post(self, request):
        bulk_action = request.POST.get("bulk_action")
        customer_lst = request.POST.getlist("selected")
        if hasattr(self, bulk_action):
            ret = getattr(self, bulk_action)(request, customer_lst)
            return ret
        else:
            return HttpResponse("操作无效")

    def bulk_del(self, requset, customer_lst):
        models.Customer.objects.filter(id__in=customer_lst).update(
            is_delete=True
        )
        if requset.path == reverse('app01:customers'):
            return redirect('app01:customers')
        else:
            return redirect('app01:mycustomers')

    @transaction.atomic
    def transfer_gs(self, requset, customer_lst):
        # customers = models.Customer.objects.filter(id__in=customer_lst)
        customers = models.Customer.objects.select_for_update().filter(id__in=customer_lst)
        msg_lst = list()
        for cus in customers:
            if cus.consultant:
                msg_lst.append(cus.name)
        models.Customer.objects.filter(id__in=customer_lst, consultant__isnull=True).update(
            consultant=models.UserInfo.objects.filter(id=requset.session.get("userid")).first()
        )
        if msg_lst:
            return self.get(requset, msg_lst)
            # return HttpResponse(msg)

        return redirect('app01:customers')

    def transfer_sg(self, requset, customer_lst):
        models.Customer.objects.filter(id__in=customer_lst).update(
            consultant=None
        )
        return redirect('app01:mycustomers')


class CustomerEditOrAdd(View):
    def get(self, request, cid=None):
        obj_list = models.Customer.objects.filter(id=cid)
        customer_modelform_obj = CustomerModelForm(request,instance=obj_list.first())
        return render(request, 'sales/customer_add.html', locals())

    def post(self, request, cid=None):
        obj_list = models.Customer.objects.filter(id=cid)
        customer_modelform_obj = CustomerModelForm(request,request.POST, instance=obj_list.first())
        if customer_modelform_obj.is_valid():
            customer_modelform_obj.save()
            return redirect(request.GET.get("next_url"))
        else:
            return render(request, 'sales/customer_add.html', locals())


def CustomerDel(request, cid):
    models.Customer.objects.filter(pk=cid).update(
        is_delete=True
    )
    return redirect(request.GET.get("next_url"))

#跟进记录相关
class ConsultRecode(View):
    def search(self, request):
        search_model = request.GET.get('search_model')  # 查询模式
        search_value = request.GET.get('search_value')  # 查询关键字
        search_uesr = request.session.get('userid')  # 查询者id
        search_customer = request.GET.get('customer_id')  # 被查询者id
        if search_model and search_value:
            all_consult_recode = models.ConsultRecord.objects.filter(delete_status=False, consultant__id=search_uesr,
                                                                     **{search_model: search_value})
        else:
            all_consult_recode = models.ConsultRecord.objects.filter(delete_status=False, consultant__id=search_uesr)

        if search_customer:
            all_consult_recode = all_consult_recode.filter(customer_id=search_customer)
        return all_consult_recode.order_by("-date"),search_value

    def get(self, request):
        all_consult_recode,search_value = self.search(request)
        page_obj = Paginaton(request.GET.get('page'), all_consult_recode.count(), request.GET)
        all_consult_recode_filter = all_consult_recode[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, 'sales/consult_recode.html', locals())

    def post(self, request):
        bulk_action = request.POST.get("bulk_action")
        recode_lst = request.POST.getlist("selected")
        if hasattr(self, bulk_action):
            ret = getattr(self, bulk_action)(request, recode_lst)
            return ret
        else:
            return HttpResponse("操作无效")

    def bulk_del(self, requset, recode_lst):
        models.ConsultRecord.objects.filter(id__in=recode_lst).update(
            delete_status=True
        )
        return redirect('app01:consult_recode')


class ConsultRecodeEditOrAdd(View):
    def get(self, request, consultrecord_id=None):
        obj_list = models.ConsultRecord.objects.filter(id=consultrecord_id)
        consult_modelform_obj = ConsultRecordModelForm(request, instance=obj_list.first())
        return render(request, 'sales/consult_recode_edit.html', locals())

    def post(self, request, consultrecord_id=None):
        obj_list = models.ConsultRecord.objects.filter(id=consultrecord_id)
        consult_modelform_obj = ConsultRecordModelForm(request, request.POST, instance=obj_list.first())
        if consult_modelform_obj.is_valid():
            consult_modelform_obj.save()
            return redirect(request.GET.get("next_url"))
        else:
            return render(request, 'sales/consult_recode_edit.html', locals())


def ConsultRecodeDel(request, cid):
    models.ConsultRecord.objects.filter(pk=cid).update(
        delete_status=True
    )
    return redirect(request.GET.get("next_url"))

#报名记录相关
class EnrollMent(View):
    def search(self, request):
        search_model = request.GET.get('search_model')  # 查询模式
        search_value = request.GET.get('search_value')  # 查询关键字
        search_uesr = request.session.get('userid')  # 查询者id
        if search_model and search_value:
            all_enrollment_recode = models.Enrollment.objects.filter(delete_status=False,
                                                                     **{search_model: search_value})
        else:
            all_enrollment_recode = models.Enrollment.objects.filter(delete_status=False,)
        return all_enrollment_recode.order_by('-enrolled_date'),search_value

    def get(self, request):
        all_enrollment_recode,search_value = self.search(request)
        page_obj = Paginaton(request.GET.get('page'), all_enrollment_recode.count(), request.GET)
        all_enrollment_recode_filter = all_enrollment_recode[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, 'sales/enrollment_list.html', locals())

    def post(self, request):
        bulk_action = request.POST.get("bulk_action")
        recode_lst = request.POST.getlist("selected")
        if hasattr(self, bulk_action):
            ret = getattr(self, bulk_action)(request, recode_lst)
            return ret
        else:
            return HttpResponse("操作无效")

    def bulk_del(self, requset, recode_lst):
        models.Enrollment.objects.filter(id__in=recode_lst).update(
            delete_status=True
        )
        return redirect('app01:enrollment')


class EnrollMentEditOrAdd(View):
    def get(self, request, form_id=None):
        obj_list = models.Enrollment.objects.filter(id=form_id)
        modelform_obj = EnrollmentModelForm(request,instance=obj_list.first())
        return render(request, 'sales/add_or_edit.html', locals())

    def post(self, request, form_id=None):
        obj_list = models.Enrollment.objects.filter(id=form_id)
        modelform_obj = EnrollmentModelForm(request,request.POST,instance=obj_list.first())
        if modelform_obj.is_valid():
            modelform_obj.save()
            return redirect(request.GET.get("next_url"))
        else:
            return render(request, 'sales/add_or_edit.html', locals())


def EnrollMentDel(request, cid):
    models.Enrollment.objects.filter(pk=cid).update(
        delete_status=True
    )
    return redirect(request.GET.get("next_url"))


class AddOrEdit(View):
    def get_obj(self,request, form_id=None):
        id = form_id
        if not id:
            id = 1
        dic = {
            reverse('app01:customer_edit', args=(id,)): [models.Customer, CustomerModelForm],
            reverse('app01:customer_add'): [models.Customer, CustomerModelForm],
            reverse('app01:consult_recode_edit', args=(id,)): [models.ConsultRecord, ConsultRecordModelForm],
            reverse('app01:consult_recode_add'): [models.ConsultRecord, ConsultRecordModelForm],
            reverse('app01:enrollment_edit', args=(id,)): [models.Enrollment, EnrollmentModelForm],
            reverse('app01:enrollment_add'): [models.Enrollment, EnrollmentModelForm],
        }

        obj_list = dic.get(request.path)[0].objects.filter(id=form_id)
        if request.method == 'GET':
            modelform_obj = dic.get(request.path)[1](request, instance=obj_list.first())
        else:
            modelform_obj = dic.get(request.path)[1](request,request.POST, instance=obj_list.first())
        return obj_list,modelform_obj


    def get(self, request, form_id=None):
        obj_list, modelform_obj = self.get_obj(request,form_id)
        return render(request, 'sales/add_or_edit.html', locals())

    def post(self, request, form_id=None):
        obj_list, modelform_obj = self.get_obj(request,form_id)
        if modelform_obj.is_valid():
            modelform_obj.save()
            return redirect(request.GET.get("next_url"))
        else:
            return render(request, 'sales/add_or_edit.html', locals())

class CourseRecordView(View):
    def get(self,request):
        courser_record_lst = models.CourseRecord.objects.all()
        return render(request,'sales/courserecode_list.html',locals())