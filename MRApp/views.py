from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
import string
import random
from MRApp.models import Userinformation, Registerinfo, Movieinformation
from django.contrib.auth import login
# Create your views here.


class LoginView(View):
    def post(self, request):
        try:
            name = request.POST.get('name', None)
            password = request.POST.get('password', None)
            print(name, password)
            code = request.POST.get('code')
            flag = Registerinfo.objects.filter(user_name=name).exists()
            if flag:
                is_register = Registerinfo.objects.filter(user_name=name, user_password=password).exists()
                if is_register:
                    response = {}
                    information = self.find_Info(name)
                    first = 0
                    type_recommend = ""
                    if information:
                        type_recommend = self.type_movie_info(information['user_hobby'])
                        first = 1
                    print(type_recommend, first)
                    response = {
                        'code': 200,
                        'message': "登录成功!",
                        'userInfo': information,
                        'first': first,
                        'type_recommend': type_recommend,
                    }
                    return JsonResponse(response)
                else:
                    return JsonResponse({'code': 400, 'message': "账户或密码错误！"})
            else:
                return JsonResponse({'code': 400, 'message': "账户不存在"})
        except:
            return JsonResponse({'code': 400, 'message': "error"})

    def find_Info(self, user):
        try:
            information = Userinformation.objects.filter(user_name=user)
            info_list = list(information.values())
            return info_list[0]
        except:
            return False

    def type_movie_info(self, types):
        types = types.split('、')
        minfo = Movieinformation.objects.all().values()
        movie_info = []
        for type in types:
            for movie in minfo:
                styles = movie["movie_style"][1:-1].replace("'", "").replace(" ", "").split(',')
                print(type, styles)
                for style in styles:
                    if style == type:
                        movie_info.append(movie)
                        if len(movie_info) == 9:
                            return movie_info
        if not movie_info:
            return "NULL"

class RegisterView(View):
    def post(self, request):
        user = Registerinfo()
        try:
            account = ''.join(random.choice(string.ascii_letters) for _ in range(2))
            account = account + ''.join(random.choice(string.digits) for _ in range(6))
            user.user_name = request.POST.get('name', None)
            user.user_password = request.POST.get('password', None)
            password = request.POST.get('password2', None)
            user.user_phone = request.POST.get('mobile', None)
            code = request.POST.get('code', None)
            f_mobile = Registerinfo.objects.filter(user_phone=user.user_phone)
            f_account = Registerinfo.objects.filter(user_account=account)
            if not f_account.exists():
                account = ''.join(random.choice(string.ascii_letters) for _ in range(2))
                account = account + ''.join(random.choice(string.digits) for _ in range(6))
            user.user_account = account

            print(user.user_name, user.user_password, password, user.user_phone, code)
            if password != user.user_password:
                return JsonResponse({'code': 400, 'message': '1数据出错！请重新输入'})
            elif not all([user.user_name, user.user_password, password, user.user_phone, code]):
                return JsonResponse({'code': 400, 'message': '2数据出错！请重新输入'})
            elif f_mobile.exists():
                return JsonResponse({'code': 400, 'message': '手机号已存在！'})
            else:
                user.save()
                return JsonResponse({'code': 200, 'message': '注册成功！'})
        except:
            return JsonResponse({'code': 400, 'message': '3数据出错！请重新输入'})




class Complete(View):
    def post(self, request):
        try:
            image = request
            print(image)
        except:
            pass