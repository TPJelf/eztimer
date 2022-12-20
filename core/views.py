# django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# app imports
from .models import *

# Libraries imports
import datetime
import zoneinfo

def login_user(request):
    if request.user.is_authenticated:
        return redirect('timer')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('timer')
        else:
            messages.error(request, 'Usuario o contraseña erróneo')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')
    

@login_required(login_url='login')
def timer(request):
  return render(request, 'timer.html')


@login_required(login_url='login')
def config(request):
  return render(request, 'config.html')




# Timezone shit
def index(request):
  request.session['django_timezone'] = request.user.userprofile.timezone.name

  user_tz = zoneinfo.ZoneInfo(request.user.userprofile.timezone.name)

  utc_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
  user_time = datetime.datetime.now().astimezone(user_tz).strftime('%Y-%m-%d %H:%M:%S')

  response_str = f'Session timezone is {request.session["django_timezone"]}. Your timezone is {request.user.userprofile.timezone.name}.\nUTC time: {utc_time}\nUser time: {user_time}'
  return HttpResponse(response_str)

def set_timezone(request):

  timezones = Timezone.objects.all()

  if request.method == 'POST':
      timezone = request.POST.get('timezone')
      userprofile = request.user.userprofile
      userprofile.timezone = Timezone.objects.get(id=timezone)
      userprofile.save()
      return redirect('/')
  else:
      return render(request, 'timezone.html', {'timezones': timezones})