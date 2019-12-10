from django import template

from django.urls import reverse

register = template.Library()


@register.filter
def customer_title(path):
    if path == reverse('app01:customers'):
        return '公户信息展示'
    else:
        return '私户信息展示'


@register.filter
def list_number(request, forloop_counter):
    current_page = request.GET.get('page')
    try:
        current_page = int(current_page)
    except:
        current_page = 1
    return (current_page - 1) * 10 + forloop_counter


@register.simple_tag
def url_encode(requset, target_url, cid,data_num=10):
    from django.http import QueryDict
    target_url = reverse(target_url, args=(cid,))
    transfer_qdict = QueryDict(mutable=True)
    obj = requset.GET.copy()
    if data_num == 1:
        try:
            obj['page'] = int(obj['page']) - 1
        except:
            pass
    transfer_qdict['next_url'] = requset.path + '?'+obj.urlencode()
    next_url = transfer_qdict.urlencode()
    fullpath = target_url + "?" + next_url
    return fullpath
