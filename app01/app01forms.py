import hashlib

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01 import models


def Md5_hash(user, pwd):
    md5 = hashlib.md5(user.encode("utf-8"))
    md5.update(pwd.encode("utf-8"))
    return md5.hexdigest()


class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed_value in self.fields.values():
            filed_value.error_messages.update({
                "required": "输入不能为空",
            })

    username = forms.CharField(
        max_length=18,
        min_length=2,
        widget=forms.TextInput(attrs={"placeholder": "您的用户名"}))
    password = forms.CharField(
        max_length=32,
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "输入密码"}),
        error_messages={
            "min_length": "密码至少6位"
        })
    confirm_password = forms.CharField(
        max_length=32,
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "再次输入密码"}),
        error_messages={
            "min_length": "密码至少6位"
        }
    )
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "输入手机号码"}),
        validators=[RegexValidator(r"^1[0-9]{10}", "手机号为长度11位的数字")])
    email = forms.EmailField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "输入邮箱地址"}),
        validators=[RegexValidator(r".*@163.com$", "邮箱必须为163邮箱")],
        error_messages={
            "invalid": "邮箱格式错误"
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            models.UserInfo.objects.get(username=username)
            self.add_error('username', '用户名重复')
            raise ValidationError('用户名重复')
        except:
            return username

    def clean(self):
        username = self.cleaned_data.get('username')
        password_value = self.cleaned_data.get('password')
        re_password_value = self.cleaned_data.get('confirm_password')
        if password_value == re_password_value:
            try:
                self.cleaned_data.update({"password": Md5_hash(username, password_value)})
            except:
                pass
            return self.cleaned_data
        else:
            self.add_error('confirm_password',
                           '两次密码不一致')
            raise ValidationError('两次密码不一致')


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed_value in self.fields.values():
            filed_value.error_messages.update({
                "required": "输入不能为空",
            })

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "用户名"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "密码"}), )

    def clean(self):

        try:
            username = self.cleaned_data.get('username')
            password = Md5_hash(username, self.cleaned_data.get('password'))
            models.UserInfo.objects.get(username=username, password=password)
            return self.cleaned_data
        except:
            self.add_error('password',
                           '账号或密码错误')
            raise ValidationError('账号或密码错误')


#customer的modelform类
class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        exclude = ['is_delete']

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            if name == 'course':
                continue
            field.widget.attrs.update({'class':'form-control'})

class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status',]

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            if name == 'customer':
                field.queryset = models.Customer.objects.filter(
                    is_delete=False,
                    consultant__id=request.session.get('userid'))
            elif name == 'consultant':
                l1 = models.UserInfo.objects.filter(id=request.session.get('userid'))
                field.choices = [(i.id, i.username) for i in l1]

            field.widget.attrs.update({'class':'form-control'})

class EnrollmentModelForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'
        exclude = ['delete_status',]

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            if name == 'customer':
                field.queryset = models.Customer.objects.filter(
                    is_delete=False).exclude(status="unregistered")
            field.widget.attrs.update({'class':'form-control'})