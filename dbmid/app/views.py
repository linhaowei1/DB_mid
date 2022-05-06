from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from app.models import Feedback
import os
def get_bardisplay(
    navbar_name,
    user_type="student",
    warn_code=None,
    warn_message=None,

):
    bar_display = {
        "navbar_name": navbar_name,
        "user_type": user_type,    
    }
    if warn_code:
        bar_display['warn_code'] = warn_code
        bar_display['warn_message'] = warn_message
    return bar_display
    
# Base class for all views (except for loginView) to enforce login
class MyView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'

class IndexView(MyView):
    def get(self, request, *args, **kwargs):
        bar_display = get_bardisplay("我的主页")
        show_feedback = True

        return render(request, 'app/index_.html', locals())
    
    def post(self, request, *args, **kwargs):
        bar_display = get_bardisplay("我的主页")

        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('app:login_view'))

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('app:login_view'))

class ModifyFeedbackView(MyView):
    def get(self, request, *args, **kwargs):
        bar_display = get_bardisplay("贴子详情")
        fid = request.GET.get('fid',None)
        warn_code = request.GET.get('warn_code',None)
        if warn_code is not None:
            bar_display['warn_code'] = int(warn_code)
            if bar_display['warn_code'] == 1:
                bar_display['warn_message'] = "请不要恶意修改url！" 
            elif bar_display['warn_code'] == 2:
                bar_display['warn_message'] = "成功创建一条帖子！"
        
        # 查找是否有get到的fid
        if fid is None:
            allow_form_edit = True
            commentable = False
        else:
            feedback = Feedback.objects.filter(fid=fid)
            # 找不到这条帖子
            if len(feedback) == 0:
                return HttpResponseRedirect(
                    reverse('app:modifyfeedback_view') + '?warn_code=1'
                )
            allow_form_edit = False
            commentable = True

        return render(request, 'app/modifyfeedback.html', locals())

    def post(self, request, *args, **kwargs):
        bar_display = get_bardisplay("贴子详情")
        # 创建一个feedback
        # fid = ?
        return HttpResponseRedirect(
            reverse('app:modifyfeedback_view') + '?warn_code=2'
        )

class LoginView(TemplateView):
    template_name = 'app/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('app:index_view'))
        else:
            return HttpResponse("Wrong username / password.")



