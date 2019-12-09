from django.db.models import *

from multiselectfield import MultiSelectField
# from django.utils.safestring import mark_safe
# from rbac.models import User

# Create your models here.


course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)
pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)


class UserInfo(Model):
    username = CharField(max_length=16, blank=False, unique=True)
    password = CharField(max_length=32, blank=False)
    telephone = CharField(max_length=20, blank=False)
    email = EmailField(max_length=50, blank=False)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.username


class Customer(Model):
    """
    客户表（最开始的时候大家都是客户，销售就不停的撩你，你还没交钱就是个客户）
    """
    qq = CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = CharField('QQ昵称', max_length=64, blank=True, null=True)  # requierd:False
    name = CharField('姓名', max_length=32, help_text='学员报名后，请改为真实姓名')  # 可为空，有些人就不愿意给自己的真实姓名
    sex_type = (('male', '男'), ('female', '女'))  #
    sex = CharField("性别", choices=sex_type, max_length=16, default='male', blank=True, null=True)  # 存的是male或者female，字符串
    birthday = DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    phone = BigIntegerField('手机号', blank=True, null=True)  # 手机号改成字符串的，不然不好搜索
    # phone = CharField('手机号', blank=True, null=True)
    source = CharField('客户来源', max_length=64, choices=source_type, default='qq')

    introduce_from = ForeignKey('self', verbose_name="转介绍自学员", blank=True, null=True,
                                on_delete=CASCADE)  # self指的就是自己这个表，和下面写法是一样的效果
    # '''
    # id  name introduce_from
    # 1   dz   None
    # 2   xf   1
    # 3   cg   1
    #
    # '''

    # introduce_from = ForeignKey('Customer', verbose_name="转介绍自学员", blank=True, null=True,on_delete=CASCADE)
    course = MultiSelectField("咨询课程", choices=course_choices)  # 多选，并且存成一个列表的格式,通过modelform来用的时候，会成为一个多选框

    # course = CharField("咨询课程", choices=course_choices) #如果你不想用上面的多选功能，可以使用Charfield来存
    class_type = CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = TextField("客户备注", blank=True, null=True, )
    status = CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",
                       help_text="选择客户此时的状态")  # help_text这种参数基本都是针对admin应用里面用的

    date = DateTimeField("咨询日期", auto_now_add=True)  # 这个没啥用昂，我问销售，销售说是为了一周年的时候给客户发一个祝福信息啥的
    last_consult_date = DateField("最后跟进日期", auto_now_add=True)  # 考核销售的跟进情况，如果多天没有跟进，会影响销售的绩效等
    next_date = DateField("预计再次跟进时间", blank=True, null=True)  # 销售自己大概记录一下自己下一次会什么时候跟进，也没啥用

    # 用户表中存放的是自己公司的所有员工。
    # related_name用于替换反向查询时，小写表名_set
    consultant = ForeignKey('UserInfo', verbose_name="销售", related_name='customers', blank=True, null=True,
                            on_delete=CASCADE)

    # 一个客户可以报多个班，报个脱产班，再报个周末班等，所以是多对多。
    class_list = ManyToManyField('ClassList', verbose_name="已报班级", blank=True)
    is_delete = BooleanField(default=False)
    class Meta:
        #配置信息
        ordering = ['id', ]#设置查询数据默认排序
        verbose_name = '客户信息表'
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return self.name + ":" + self.qq

    # enroll_status_choices = (('signed', "已报名"),
    #                          ('unregistered', "未报名"),
    #                          ('studying', '学习中'),
    #                          ('paid_in_full', "学费已交齐"))
    #
    # def status_show(self):
    #     status_color = {
    #         'paid_in_full': 'green',
    #         'unregistered': 'red',
    #         'studying': 'lightblue',
    #         'signed': 'yellow',
    #     }
    #
    #     return mark_safe("<span style='background-color:{0}'>{1}</span>".format(status_color[self.status],
    #                                                                             self.get_status_display()))
    # def get_classlist(self):  #当我们通过self.get_classlist的时候，就拿到了所有的班级信息，前端显示的时候用
    #
    #     l=[]
    #     for cls in self.class_list.all():
    #         l.append(str(cls))
    #     return mark_safe(",".join(l)) #纯文本，不用mark_safe也可以昂


class Campuses(Model):
    """
    校区表
    """
    name = CharField(verbose_name='校区', max_length=64)
    address = CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class ClassList(Model):
    """
    班级表
    """
    course = CharField("课程名称", max_length=64, choices=course_choices)
    semester = IntegerField("学期")  # python20期等
    campuses = ForeignKey('Campuses', verbose_name="校区", on_delete=CASCADE)
    price = IntegerField("学费", default=10000)
    memo = CharField('说明', blank=True, null=True, max_length=100)
    start_date = DateField("开班日期")
    graduate_date = DateField("结业日期", blank=True, null=True)  # 不一定什么时候结业，哈哈，所以可为空

    # contract = ForeignKey('ContractTemplate', verbose_name="选择合同模版", blank=True, null=True,on_delete=CASCADE)
    teachers = ManyToManyField('UserInfo', verbose_name="老师")  # 对了，还有一点，如果你用的django2版本的，那么外键字段都需要自行写上on_delete=CASCADE

    class_type = CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True, null=True)

    class Meta:
        unique_together = ("course", "semester", 'campuses')

    def __str__(self):
        return "{}{}({})".format(self.get_course_display(), self.semester, self.campuses)


############################下面的表以后再说#################################

# class ContractTemplate(Model):
#     """
#     合同模板表
#     """
#     name = CharField("合同名称", max_length=128, unique=True)
#     content = TextField("合同内容")
#     date = DateField(auto_now=True)
#
#

# class ConsultRecord(Model):
#     """
#     跟进记录表
#     """
#     customer = ForeignKey('Customer', verbose_name="所咨询客户")
#     note = TextField(verbose_name="跟进内容...")
#     status = CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")
#     consultant = ForeignKey("UserInfo", verbose_name="跟进人", related_name='records')
#     date = DateTimeField("跟进日期", auto_now_add=True)
#     delete_status = BooleanField(verbose_name='删除状态', default=False)
#     # def __str__(self):
#
#
# class Enrollment(Model):
#     """
#     报名表
#     """
#     why_us = TextField("为什么报名", max_length=1024, default=None, blank=True, null=True)
#     your_expectation = TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)
#     # contract_agreed = BooleanField("我已认真阅读完培训协议并同意全部协议内容", default=False)
#     contract_approved = BooleanField("审批通过", help_text="在审阅完学员的资料无误后勾选此项,合同即生效", default=False)
#     enrolled_date = DateTimeField(auto_now_add=True, verbose_name="报名日期")
#     memo = TextField('备注', blank=True, null=True)
#     delete_status = BooleanField(verbose_name='删除状态', default=False)
#     customer = ForeignKey('Customer', verbose_name='客户名称')
#     school = ForeignKey('Campuses')
#     enrolment_class = ForeignKey("ClassList", verbose_name="所报班级")
#
#     class Meta:
#         unique_together = ('enrolment_class', 'customer')
#
#     def __str__(self):
#         return self.customer.name
#
#
# # class PaymentRecord(Model):
# #     """
# #     缴费记录表
# #     """
# #     pay_type = CharField("费用类型", choices=pay_type_choices, max_length=64, default="deposit")
# #     paid_fee = IntegerField("费用数额", default=0)
# #     note = TextField("备注", blank=True, null=True)
# #     date = DateTimeField("交款日期", auto_now_add=True)
# #     course = CharField("课程名", choices=course_choices, max_length=64, blank=True, null=True, default='N/A')
# #     class_type = CharField("班级类型", choices=class_type_choices, max_length=64, blank=True, null=True,
# #                                   default='N/A')
# #     enrolment_class = ForeignKey('ClassList', verbose_name='所报班级', blank=True, null=True)
# #     customer = ForeignKey('Customer', verbose_name="客户")
# #     consultant = ForeignKey('UserProfile', verbose_name="销售")
# #     delete_status = BooleanField(verbose_name='删除状态', default=False)
# #
# #     status_choices = (
# #         (1, '未审核'),
# #         (2, '已审核'),
# #     )
# #     status = IntegerField(verbose_name='审核', default=1, choices=status_choices)
# #
# #     confirm_date = DateTimeField(verbose_name="确认日期", null=True, blank=True)
# #     confirm_user = ForeignKey(verbose_name="确认人", to='UserProfile', related_name='confirms', null=True,
# #                                      blank=True)
# #
# #
#
# # course_record_id   student   考勤   本节成绩   homework_note
# # #  1                 74       crm          跟进记录操作   1  迟到    60          写的很好
# # #  1                 74       crm          跟进记录操作   2  签到    80          写的非常好
# # #
# # # id 节次   本节课程标题   本节课程内容
# # # 1 74       crm          跟进记录操作
#
#
# class CourseRecord(Model):
#     """课程记录表"""
#     day_num = IntegerField("节次", help_text="此处填写第几节课或第几天课程...,必须为数字")
#     date = DateField(auto_now_add=True, verbose_name="上课日期")
#     course_title = CharField('本节课程标题', max_length=64, blank=True, null=True)
#     course_memo = TextField('本节课程内容', max_length=300, blank=True, null=True)
#     has_homework = BooleanField(default=True, verbose_name="本节有作业")
#     homework_title = CharField('本节作业标题', max_length=64, blank=True, null=True)
#     homework_memo = TextField('作业描述', max_length=500, blank=True, null=True)
#     scoring_point = TextField('得分点', max_length=300, blank=True, null=True)
#
#     re_class = ForeignKey('ClassList', verbose_name="班级")
#     teacher = ForeignKey('UserInfo', verbose_name="讲师")
#
#     class Meta:
#         unique_together = ('re_class', 'day_num')
#
#     def __str__(self):
#         return str(self.day_num)
#
#
# class StudyRecord(Model):
#     """
#     学习记录
#     """
#     attendance = CharField("考勤", choices=attendance_choices, default="checked", max_length=64)
#     score = IntegerField("本节成绩", choices=score_choices, default=-1)
#     homework_note = CharField(max_length=255, verbose_name='作业批语', blank=True, null=True)
#     date = DateTimeField(auto_now_add=True)
#     note = CharField("备注", max_length=255, blank=True, null=True)
#     homework = FileField(verbose_name='作业文件', blank=True, null=True, default=None)
#     course_record = ForeignKey('CourseRecord', verbose_name="某节课程")
#     student = ForeignKey('Customer', verbose_name="学员")
#
#     class Meta:
#         unique_together = ('course_record', 'student')
#
#     def __str__(self):
#         return self.student.name + ':' + str(self.course_record.day_num)
