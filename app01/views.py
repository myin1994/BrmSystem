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

class Login(View):
    def get(self,request):
        return render(request,'auth/login.html')


class Register(View):
    def get(self,request):
        return render(request,'auth/register.html')