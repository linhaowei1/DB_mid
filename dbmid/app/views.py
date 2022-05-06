from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

# Base class for all views (except for loginView) to enforce login
class MyView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'


class IndexView(MyView):
    template_name = 'app/index.html'
    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('app:login_view'))


class LoginView(TemplateView):
    template_name = 'app/login.html'

    def post(self, request, *args, **kwargs):
        print(*args, **kwargs)
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('app:index_view'))
        else:
            return HttpResponse("Wrong username / password.")



