import json,datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render_to_response, render
from .models import *
from django.db import transaction

def register(request):

    jsonObj = json.loads(request.body)
    email = jsonObj.get('email')
    mobile_no = str(jsonObj.get('mobileNo')) if jsonObj.get('mobileNo') else None
    password = jsonObj.get('password')

    if not email and not mobile_no:
        return HttpResponse(json.dumps({"validation": "Enter email id or mobile no", "status": False}), content_type="application/json")

    username = ''
    if email:
        username = username + email

    if mobile_no:
        username = username + mobile_no

    if not password:
        return HttpResponse(json.dumps({"validation": "Enter password", "status": False}), content_type="application/json")

    if User.objects.filter(username=username).exists():
        return HttpResponse(json.dumps({"validation": "User already exists in system", "status": False}), content_type="application/json")

    try:
        with transaction.atomic():
            user = User()
            user.username = username
            user.set_password(password)
            user.save()

            reg = Registration()
            reg.user = user
            reg.email = email
            reg.mobile_no = mobile_no
            reg.save()
        return HttpResponse(json.dumps({"validation": "User Registered Successfully", "status": True}), content_type="application/json")
    except Exception as e:
        print e
        return HttpResponse(json.dumps({"validation": "Failed to register a user", "status": False}), content_type="application/json")

def login_view(request):
    jsonObj = json.loads(request.body)
    email = jsonObj.get('email')
    mobile_no = str(jsonObj.get('mobileNo')) if jsonObj.get('mobileNo') else None
    password = jsonObj.get('password')

    if not email and not mobile_no:
        return HttpResponse(json.dumps({"validation": "Enter email id or mobile no", "status": False}), content_type="application/json")

    if not password:
        return HttpResponse(json.dumps({"validation": "Enter password", "status": False}), content_type="application/json")

    if email:
        try:
            reg = Registration.objects.get(email=email)
        except Exception as e:
            return HttpResponse(json.dumps({"validation": "User not found", "status": False}), content_type="application/json")
    elif mobile_no:
        try:
            reg = Registration.objects.get(mobile_no=mobile_no)
        except Exception as e:
            return HttpResponse(json.dumps({"validation": "User not found", "status": False}), content_type="application/json")

    username = ''
    if reg.email:
        username = username + reg.email

    if reg.mobile_no:
        username = username + reg.mobile_no

    user = authenticate(username=username, password=password)
    if not user:
        return HttpResponse(json.dumps({"validation": "Incorrect password", "status": False}), content_type="application/json")

    login(request, user)
    user_data = {}
    user_data['userId'] = reg.user.id
    user_data['username'] = reg.user.username
    user_data['email'] = reg.email
    user_data['mobile_no'] = reg.mobile_no
    return HttpResponse(json.dumps({"validation": "User logged in successfully", "data": user_data, "status": True}), content_type="application/json")
