from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy

# Create your views here.
from .models import UserProfile

def login(request):
    error_msg = ''
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = UserProfile.objects.filter(email=email, password=password).first()
        if user:
            request.session["user_id"] = user.pk
            return redirect(reverse('userall'))
        error_msg = "用户名或密码错误"
    return render(request, 'login.html',{"error_msg":error_msg})


def logout_view(request):
    request.session.flush()
    return redirect(reverse('login'))