import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse


class Login_sign(MiddlewareMixin):
    white_list = [reverse("app01:login"),reverse("app01:register"),'/admin/.*']
    def process_request(self,request):
        current_path = request.path
        for path in self.white_list:
            if re.match(f"^{path}$",current_path):
                return None
        else:
            login_status = request.session.get("status")
            if login_status == "success":
                return None
            else:
                return redirect("app01:login")


