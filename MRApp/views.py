import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
import string
import random
from MRApp.models import *
from django.contrib.auth import login
from MRApp.collaborative_filtering import recommend
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
                    # recommend = self.movie_recommend(information.get('user_account_id'))
                    print(recommend)
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
                for style in styles:
                    if style == type:
                        movie_info.append(movie)
                        if len(movie_info) == 40:
                            return movie_info
        if not movie_info:
            return "NULL"


    def movie_recommend(self, userID):
        movies = []
        surf_all = Surfinformation.objects.filter(user=userID).values()
        surf_movie = []
        for surf in surf_all:
            surf_movie.append(np.int32(surf['movie_id']))
        movies.append(surf_movie)
        fav_all = Favoriteinformation.objects.filter(user=userID).values()
        fav_movie = []
        for fav in fav_all:
            fav_movie.append(np.int32(fav['movie_id']))
        movies.append(fav_movie)
        sco_all = Scoreinformation.objects.filter(user=userID).values()
        sco_movie = []
        for sco in sco_all:
            sco_movie.append((userID, np.int32(sco["movie_id"]), np.float32(sco["movie_score"])))
        movies.append(sco_movie)
        print(movies)
        movie_recommend = recommend(movies)[userID]
        final_movie = []
        print(1111111111)
        for movie_id in movie_recommend:
            final_movie.append(Movieinformation.objects.filter(movie_id=movie_id).values()[0])
        return final_movie


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



class get_movie_info(View):
    def post(self, request):
        try:
            movieID = request.POST.get('id')
            print(movieID, type(movieID))
            movie = Movieinformation.objects.filter(movie_id=movieID).values()
            print(movie)
            if movie:
                movie_info = list(movie)
                name = movie_info[0].get('movie_name') + " "
                print(name, 111111)
                comments = Moviecomments.objects.filter(movie_name=name).values()

                print(comments)

                return JsonResponse({'code': 200, 'movie': movie_info[0]})
        except:
            print(2222222)
            pass


def get_all_movie(request):
    try:
        type = request.POST.get('type')
        year = request.POST.get('year')
        region = request.POST.get('region')
        movies = Movieinformation.objects.all().values()
        item = []
        for movie in movies:
            styles = movie["movie_style"][1:-1].replace("'", "").replace(" ", "").split(',')
            if type in styles or type == "全部类型":
                if year == "全部年份" or year == movie['movie_year']:
                    if region == "全部国家" or region == movie["movie_country"]:
                        item.append(movie)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        print(item)
    except:
        pass

#
#
#
#
#
# def movie_info(request):#电影信息
#     surf_all = Movieinformation.objects.all().values()
#     surf_movie = []
#     for surf in surf_all:
#         surf_movie.append(np.int32(surf['movie_id']))
#     # print(surf_movie)
#     surf_movies = []
#     for mid in surf_movie[:100]:
#         tmp = Movieinformation.objects.filter(movie_id=mid).values()[0]
#         if len(tmp["movie_name"]) > 10:
#             tmp["movie_name"] = tmp["movie_name"][:9] + '...'
#         surf_movies.append(tmp)
#
#     return render(request, 'Surf_movie.html', {'surfmovie': surf_movies})
#
# def surf_movie(request):#用户浏览信息
#     uid = 'OB324390'
#     surf_all = Surfinformation.objects.filter(user_id=uid).values()
#     surf_movie = []
#     for surf in surf_all:
#         surf_movie.append(np.int32(surf['movie_id']))
#     # print(surf_movie)
#     surf_movies = []
#     for mid in surf_movie:
#         # movie_info=Movieinformation.objects.filter(movie_id=mid).values()[0]
#         # name=movie_info["user_name"]
#         tmp = Movieinformation.objects.filter(movie_id=mid).values()[0]
#         if len(tmp["movie_name"]) > 10:
#             tmp["movie_name"] = tmp["movie_name"][:9] + '...'
#         surf_movies.append(tmp)
#
#     return render(request, 'Surf_movie.html', {'surfmovie':surf_movies})
#
# def favo_movie(request):  # 用户收藏信息
#     uid = 'OB324390'
#     fav_all = Favoriteinformation.objects.filter(user_id=uid).values()
#     fav_movie = []
#     for surf in fav_all:
#         fav_movie.append(np.int32(surf['movie_id']))
#     # print(surf_movie)
#     favo_movies = []
#     for mid in fav_movie:
#         tmp = Movieinformation.objects.filter(movie_id=mid).values()[0]
#         if len(tmp["movie_name"]) > 10:
#             tmp["movie_name"] = tmp["movie_name"][:9] + '...'
#         favo_movies.append(tmp)
#
#     return render(request, 'Favo_movie.html', {'favomovie': favo_movies})
#
#
# def eva_movie(request):  # 用户评分信息
#     uid = 'OB324390'
#     eva_all = Scoreinformation.objects.filter(user_id=uid).values()
#     eva_movie = []
#     for surf in eva_all:
#         eva_movie.append(np.int32(surf['movie_id']))
#     # print(surf_movie)
#     eva_movies = []
#     for mid in eva_movie:
#         tmp = Movieinformation.objects.filter(movie_id=mid).values()[0]
#         if len(tmp["movie_name"]) > 10:
#             tmp["movie_name"] = tmp["movie_name"][:9] + '...'
#         eva_movies.append(tmp)
#
#     return render(request, 'Eva_movie.html', {'evamovie': eva_movies})
#
#
# def user_info(request):
#     # 用户个人信息
#     uid = 'OB324390'
#
#     u_info=Userinformation.objects.filter(user_account=uid).values()
#     user_infos = []
#     user_infos.append(u_info[0])
#
#     # 用户浏览信息
#     surf_all = Surfinformation.objects.filter(user_id=uid).values()
#     surf_movie = []
#     for surf in surf_all:
#         surf_movie.append(np.int32(surf['movie_id']))
#     # print(surf_movie)
#     surf_movies = []
#     for mid in surf_movie[:6]:
#         tmp = Movieinformation.objects.filter(movie_id=mid).values()[0]
#         if len(tmp["movie_name"]) > 10:
#             tmp["movie_name"] = tmp["movie_name"][:9] + '...'
#         surf_movies.append(tmp)
#
#     # 用户收藏信息
#     favo_all = Favoriteinformation.objects.filter(user_id=uid).values()
#     favo_movie = []
#     for favo in favo_all:
#         favo_movie.append(np.int32(favo['movie_id']))
#     # print(surf_movie)
#     favo_movies = []
#     for mid in favo_movie[:6]:
#         tmp = Movieinformation.objects.filter(movie_id=mid).values()[0]
#         if len(tmp["movie_name"]) > 10:
#             tmp["movie_name"] = tmp["movie_name"][:9] + '...'
#         favo_movies.append(tmp)
#
#     # 用户评分信息
#     # eva_all = Scoreinformation.objects.filter(user_id=uid).values()
#     # eva_movie = []
#     # for eva in eva_all:
#     #     eva_movie.append(np.int32(eva['movie_id']))
#     # # print(surf_movie)
#     eva_movies = []
#     for mid in eva_movie[:3]:
#         tmp = Movieinformation.objects.filter(movie_id=mid).values()[0]
#         if len(tmp["movie_name"]) > 10:
#             tmp["movie_name"] = tmp["movie_name"][:9] + '...'
#         eva_movies.append(tmp)
#
#     return render(request, 'Personal_center.html', {'userinfo':user_infos,'surfmovie':surf_movies,'favomovie':favo_movies,'evamovie':eva_movies})
#
