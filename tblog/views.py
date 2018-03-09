from django.shortcuts import render,HttpResponse
from tblog import  models
from tblog.utils import make_valid
import json
from django.contrib import auth
from tblog import uforms
from django.http import JsonResponse
# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get("user")
        password = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code").lower()
        save_session = request.session.get("keep_valid_codes").lower()
        login_response = {"user": None, "error_msg": ""}
        if save_session == valid_code:
            user=auth.authenticate(username=username,password=password)
            if user:
                auth.login(request, user)
                login_response["user"] = user.username
            else:
                login_response["error_msg"] = "error username or password"
        else:
            login_response["error_msg"] = "error valid code"
        return HttpResponse(json.dumps(login_response))


    return render(request,"login.html")

def get_valid_img(request):

    data = make_valid.get_valid(request)
    return HttpResponse(data)

def index(request):
    print("==", request.user)

    article_list = models.Article.objects.all()
    return render(request,"index.html",{"article_list":article_list})

def register(request):

    if request.method == "POST":
        valid_obj = uforms.regFrom(request.POST)
        reg_response = {"user": None, "error_mes": None}
        if valid_obj.is_valid():
            user = valid_obj.cleaned_data.get("user")
            pwd = valid_obj.cleaned_data.get("pwd")
            email = valid_obj.cleaned_data.get("email")
            avatar_img = request.FILES.get("avatar_img")
            if avatar_img:
                print("avatar_img....", avatar_img)
                user = models.UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar_img)
            else:
                user = models.UserInfo.objects.create_user(username=user, password=pwd, email=email)

            reg_response["user"] = user.username

        else:
            reg_response["error_mes"] = valid_obj.errors

        return JsonResponse(reg_response)
    else:

        form_obj = uforms.regFrom()
        return render(request, "reg.html", {"form_obj": form_obj})