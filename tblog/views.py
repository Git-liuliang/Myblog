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



def home_site(request,username,**kwargs):
    print("kwargs", kwargs)
    print(username)
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("<h3>404</h3>")

    blog = user.blog

    if not kwargs:
        article_list = models.Article.objects.filter(user=user)
    else:
        condition = kwargs.get("condition")
        param = kwargs.get("param")  # 2018-02
        if condition == "cate":
            article_list = models.Article.objects.filter(user=user).filter(homeCategory__title=param)
        elif condition == "tag":
            article_list = models.Article.objects.filter(user=user).filter(tags__title=param)
        else:
            year, month = param.split("-")
            article_list = models.Article.objects.filter(user=user).filter(create_time__year=year, create_time__month=month)

    from django.db.models import Count, Max
    cate_list = models.Category.objects.filter(blog=blog).annotate(count=Count("article")).values_list("title", "count")
    print(cate_list)

    # 查询当前站点的每一个标签的名称以及对应的文章数：分组查询
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count=Count("article")).values_list("title", "count")
    print(tag_list)

    # 日期归档
    date_list = models.Article.objects.filter(user=user).extra(
        select={"archive_date": "strftime('%%Y-%%m',create_time)"}).values("archive_date").annotate(
        c=Count("nid")).values_list("archive_date", "c")
    print(date_list)

    return render(request, "home_site.html", locals())


def get_data(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    from django.db.models import Count, Max
    cate_list = models.Category.objects.filter(blog=blog).annotate(count=Count("article")).values_list("title", "count")
    print(cate_list)
    # 查询当前站点的每一个标签的名称以及对应的文章数：分组查询
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count=Count("article")).values_list("title", "count")
    print(tag_list)
    # 日期归档
    date_list = models.Article.objects.filter(user=user).extra(
        select={"archive_date": "strftime('%%Y-%%m',create_time)"}).values("archive_date").annotate(
        c=Count("nid")).values_list("archive_date", "c")
    print(date_list)
    return {"username": username, "blog": blog, "cate_list": cate_list, "tag_list": tag_list, "date_list": date_list}


def article_detail(request,username,article_id):

    ret=get_data(username)

    article_obj=models.Article.objects.filter(pk=article_id).first()

    ret["article_obj"]=article_obj

    return render(request,"artcile_detail.html",ret)

def updown(request):
    if request.method == "POST":
        article_id = request.POST.get("article_id")
        boolen = request.POST.get("boolen")
        user = models.UserInfo.objects.filter(username=request.user.username).first()
        print(user.nid)
        print(request.POST.get("article_id"))
        print(request.POST.get("boolen"))
        print(request.user.username)
        ret = models.ArticleUpDown.objects.filter(article_id=article_id,user_id=user.nid).first()
        print(ret)
        print(type(boolen))
        if  not ret:
            models.ArticleUpDown.objects.create(article_id=article_id,is_up=boolen,user_id=user.nid)
            if boolen == "0":

                upnum = models.Article.objects.filter(nid=article_id).first().up_count
                print(upnum)
                models.Article.objects.filter(nid=article_id).update(up_count=upnum+1)
                response = {"upnum":upnum+1,"mes":"up+1"}
                return HttpResponse(json.dumps(response))
            else:
                downnum = models.Article.objects.filter(nid=article_id).first().down_count
                models.Article.objects.filter(nid=article_id).update(down_count=downnum + 1)
                response = {"downnum": downnum+1, "mes": "down+1"}
                return HttpResponse(json.dumps(response))
        else:
            response = {"mes":"您已经推荐过了！"}
            return HttpResponse(json.dumps(response))
    return HttpResponse("ok")



