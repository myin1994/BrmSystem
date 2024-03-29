from django import template
from django.urls import reverse
register = template.Library()


@register.filter
def page_title(path):
    dic = {
        reverse('app01:customers'):'公户信息展示',
        reverse('app01:mycustomers'):'私户信息展示',
        reverse('app01:consult_recode'):'跟进记录',
        reverse('app01:enrollment'):'报名记录',
        reverse('app01:courserecord'):'课程记录',
    }

    return dic.get(path, '未知页面')

@register.filter
def add_or_edit_title(path,id=1):
    if not id:
        id = 1
    dic = {
        reverse('app01:customer_edit',args=(id,)):'编辑客户页面',
        reverse('app01:customer_add'):'添加客户页面',
        reverse('app01:consult_recode_edit',args=(id,)):'编辑跟进记录页面',
        reverse('app01:consult_recode_add'):'添加跟进记录页面',
        reverse('app01:enrollment_edit',args=(id,)):'编辑报名记录页面',
        reverse('app01:enrollment_add'):'添加报名记录页面',
        reverse('app01:courserecord_edit', args=(id,)): '编辑课程记录页面',
        reverse('app01:courserecord_add'): '添加课程记录页面',
        reverse('app01:studyrecord', args=(id,)): '学习记录页面',
           }

    return dic.get(path,'还未配置')

@register.filter
def list_number(request, forloop_counter):
    current_page = request.GET.get('page')
    try:
        current_page = int(current_page)
    except:
        current_page = 1
    return (current_page - 1) * 10 + forloop_counter


@register.simple_tag
def url_encode(requset, target_url, cid='',data_num=10):
    from django.http import QueryDict

    transfer_qdict = QueryDict(mutable=True)
    obj = requset.GET.copy()
    if data_num == 1:
        try:
            obj['page'] = int(obj['page']) - 1
        except:
            pass
    if cid == '':
        target_url = reverse(target_url)
        transfer_qdict['next_url'] = requset.get_full_path()
    else:
        target_url = reverse(target_url, args=(cid,))
        transfer_qdict['next_url'] = requset.path + '?'+obj.urlencode()
    next_url = transfer_qdict.urlencode()
    fullpath = target_url + "?" + next_url
    return fullpath
