from django.db.models import *

# Create your models here.
class Role(Model):
    """
    角色表，与权限多对多
    """
    role_name = CharField(max_length=32,verbose_name='角色')
    permissions = ManyToManyField('Permission')
    def __str__(self):
        return self.role_name

class UserInfo(Model):
    """
    用户表，与角色多对多
    """
    # username = CharField(max_length=32)
    # password = CharField(max_length=32)
    roles = ManyToManyField(Role)
    # def __str__(self):
    #     return self.username

    class Meta:
        abstract = True




class TopMenu(Model):
    title = CharField(max_length=32,verbose_name='菜单名称')
    icon = CharField(max_length=32, null=True, blank=True,verbose_name='图标')
    #权重：用于展示顺序
    weight = IntegerField(default=10,verbose_name='权重')
    def __str__(self):
        return self.title


class Permission(Model):
    """
    权限表，与父级菜单多对一，功能与自己多对多
    """
    url = CharField(max_length=2083,verbose_name='权限路径')
    url_name = CharField(max_length=32, null=True, blank=True,verbose_name='路径别名')
    access_name = CharField(max_length=32,verbose_name='权限名')

    icon = CharField(max_length=32, null=True, blank=True,verbose_name='图标')
    menu = ForeignKey('TopMenu',null=True,blank=True,verbose_name='一级菜单')
    parent = ForeignKey('self', null=True, blank=True,verbose_name='父级菜单')
    weight = IntegerField(default=10,verbose_name='权重')
    def __str__(self):
        return self.access_name