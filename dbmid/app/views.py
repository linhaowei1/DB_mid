from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from app.constant import *
from django.views.generic import TemplateView
from app.models import Feedback, Organization, Comment
from app.utils import get_student_or_teacher, get_bardisplay, get_user_nickname

# Base class for all views (except for loginView) to enforce login
class MyView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'

class IndexView(MyView):
    def get(self, request, *args, **kwargs):
        user_type, person = get_student_or_teacher(request.user)
        is_student = (user_type == UserType.STUDENT)
        bar_display = get_bardisplay("我的主页")
        public_feedback = Feedback.objects.all()
        if not is_student:
            my_feedback = Feedback.objects.all().filter(
                receiver=person.organization
            )
        else:
            my_feedback = Feedback.objects.all().filter(
                poster=person
            )
        return render(request, 'app/index_.html', locals())
    
    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('app:logout_view'))

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('app:login_view'))

class ModifyFeedbackView(MyView):
    def get(self, request, *args, **kwargs):
        nickname = get_user_nickname(request.user)

        bar_display = get_bardisplay("贴子详情")
        fid = request.GET.get('fid',None)
        warn_code = request.GET.get('warn_code',None)
        if warn_code is not None:
            bar_display['warn_code'] = int(warn_code)
            if bar_display['warn_code'] == 1:
                bar_display['warn_message'] = "请不要恶意修改url！" 
            elif bar_display['warn_code'] == 2:
                bar_display['warn_message'] = "成功创建一条帖子！"
        org_list = {
            org.oname:{
                'value'   : org.oname,
                'display' : org.oname,  # 前端呈现的使用量
                'disabled' : False,  # 是否禁止选择这个量
                'selected' : False   # 是否默认选中这个量
            }
            for org in Organization.objects.all()
        }
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
            feedback = Feedback.objects.get(fid=fid)
            org_list[feedback.receiver.oname]['selected'] = True

            # prepare local var for comments
            def is_highlight(comment, feedback):
                type, user = get_student_or_teacher(comment.commenter)
                if type == UserType.TEACHER and user.organization_id == feedback.receiver.organization_id:
                    print(1)
                    return True
                return False
            comments = [{'commenter':get_user_nickname(c.commenter),
                         'time': c.public_time,
                         'content': c.content,
                         'highlight': is_highlight(c, feedback)}
                        for c in Comment.objects.filter(post=feedback)]
            allow_form_edit = False
            commentable = True

        return render(request, 'app/modifyfeedback.html', locals())

    def post(self, request, *args, **kwargs):
        # comment creation
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('app:logout_view'))
        if 'comment' in request.POST.keys():
            fid=request.GET.get('fid', None)
            comment = Comment.objects.create(
                commenter=request.user,
                post=Feedback.objects.get(fid=fid),
                content=request.POST['comment'],
            )
            return HttpResponseRedirect(
                reverse('app:modifyfeedback_view') + f'?fid={fid}'
            )
        # feedback creation
        else:
            nickname = get_user_nickname(request.user)
            bar_display = get_bardisplay("贴子详情")
            # 创建一个feedback
            # fid = ?
            student = get_student_or_teacher(request.user)[1]
            organization = Organization.objects.get(oname=request.POST['org'])
            content = request.POST['content']
            title = request.POST['title']
            feedback = Feedback.objects.create(
                poster=student,
                receiver=organization,
                title=title if title != "" else "N/A",
                content=content if content != "" else "N/A",
            )
            return HttpResponseRedirect(
                reverse('app:modifyfeedback_view') + f'?fid={feedback.fid}' + '&warn_code=2'
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



