from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from . import models
from . models import Userprofile
from . import forms
import hashlib
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):   #生成的验证码以用户名+时间戳 生成的hash代码，后面网邮件里发的链接，携带hash代码，发到指定验证的url验证
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自"中华大西瓜"的注册确认邮件'

    text_content = '''
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('www.daxigua.asia:82', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@login_required
def index(request):
    # if not request.session.get('is_login', None):
    # if request.COOKIES.get("is_login",None):
        # return redirect('/login/')
    return render(request, 'login/index.html')
    # return redirect ("/")


def login(request):
    # if not request.session.get('is_login', None):  # 代码后面设置了，如果登陆成功，session里会加入is_login，不允许重复登录
    # if request.COOKIES.get("is_login",None):
    #     return redirect('/')
    ssession_look = request.session.flush()
    cookie_look = request.COOKIES
    print("ssession_look",ssession_look)
    print("cookie_look",cookie_look)
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)   #把request.POST转成form表单类
        message = '请检查填写的内容！'  
        if login_form.is_valid():  #cleaned_data  {'password': '1245', 'username': 'QQQ', 'captcha': ['90392e2c93228b7fc4cafc438df139659a715991', '']}
            username = login_form.cleaned_data.get('username')   #cleaned_data: html中input标签里输入的内容，字典类型,input标签中，name=username
            password = login_form.cleaned_data.get('password')
            # try:
            #     user = models.Userprofile.objects.get(Q(username=username) | Q(mobile=username))   #将表单验证过的数据拿出来，创建models
            # except :
            #     message = '用户不存在！'    #通过locals() 传入模板中的{{ message }}
            #     return render(request, 'login/login.html', locals())

            # if not Userprofile.has_confirmed:   #判断user的has_confirmed字段
            #     message = '该用户还未经过邮件确认！'
            #     return render(request, 'login/login.html', locals())
            user = authenticate(username=username, password=password)
            if user:
            # if Userprofile.password == hash_code(password) or user.password == password:  #用户、有限认证、密码都通过后，设置session里字典内容
                auto_login(request, user)
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                print("auth/////////////")
                # reverse('reverse:userInfo',kwargs={'user_id':10})
                url = reverse("blog:index")
                print(url)
                response = redirect(url)
                # response.set_signed_cookie("is_login",True,salt="blog")
                # response.set_signed_cookie("user_id",user.id,salt="blog")
                # response.set_signed_cookie("user_name",user.username,salt="blog")
                return response
            else:
                message = '密码不正确！'  
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()   #清空login_form变量 内容
    return render(request, 'login/login.html', locals())   #locals会把本地变量，此处有message、login_form、username、password变量传入模板中


def register(request):
    # if not request.session.get('is_login', None):
    if request.COOKIES.get("is_login",None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            mobile = register_form.cleaned_data.get('mobile')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.Userprofile.objects.filter(username=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.Userprofile.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())
                same_mobile_user = models.Userprofile.objects.filter(mobile=mobile)
                if same_mobile_user:
                    message = '该手机号已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.Userprofile()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.mobile = mobile
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')

    request.session.flush()  #登陆退出，消除session
    # del request.session['is_login']
    print('logout...........')
    return redirect("/login/login")


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''

    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True     #联表查询
        confirm.user.save() #把user保存
        confirm.delete()   #把验证实例删掉
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
