from django.utils import timezone

import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
import string
import random

from requests import Response

from MRApp.models import *
from django.contrib.auth import login
from MRApp.collaborative_filtering import recommend
from MRApp.check_code import create_validate_code
# Create your views here.


def set_face(request):
    print(request)
    return JsonResponse({ 'code': 200 })

def get_images(request):

    img, person_codes = create_validate_code()
    img.save(r'D:/Code/Idea/client/src/assets/code.jpg')

    return JsonResponse({"code": person_codes})

def Login(request):
    try:
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)
        print(name, password)
        flag = Registerinfo.objects.filter(user_name=name).exists()
        if flag:
            is_register = Registerinfo.objects.filter(user_name=name, user_password=password).exists()
            if is_register:
                response = {}
                information = find_Info(name)
                first = 0
                type_recommend = ""
                if information:
                    print(111111111)
                    type_recommend = type_movie_info(information['user_hobby'])
                    first = 1
                    print(222222222, type_recommend, first)
                    recommend = movie_recommend(information['user_account'])
                    print(recommend)
                    response = {
                        'code': 200,
                        'message': "登录成功!",
                        'userInfo': information,
                        'first': first,
                        'type_recommend': type_recommend,
                        'recommend': recommend,
                    }
                    return JsonResponse(response)
                else:
                    return JsonResponse({'code': 200, 'message': "请完善个人信息!", 'first': first})
            else:
                return JsonResponse({'code': 400, 'message': "账户或密码错误！"})
        else:
            return JsonResponse({'code': 400, 'message': "账户不存在"})
    except:
        return JsonResponse({'code': 400, 'message': "error"})

def find_Info(user):
    try:
        information = Userinformation.objects.filter(user_name=user)
        print(information)
        info_list = list(information.values())
        print(info_list)
        return info_list[0]
    except:
        return False

def type_movie_info(types):
    types = types.split(',')
    print(types)
    minfo = Movieinformation.objects.all().values()
    movie_info = []
    for type in types:
        for movie in minfo:
            styles = movie["movie_style"][1:-1].replace("'", "").replace(" ", "").split(',')
            for style in styles:
                if style == type:
                    movie_info.append(movie)
                    if len(movie_info) == 50:
                        return movie_info
    if not movie_info:
        return "NULL"


def movie_recommend(userID):
    movies = []
    surf_all = Surfinformation.objects.filter(user_id=userID).values()

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
    movie_recommend = recommend(movies)[userID]

    final_movie = []
    for movie_id in movie_recommend:
        final_movie.append(Movieinformation.objects.filter(movie_id=movie_id).values()[0])
    return final_movie


def RegisterView(request):
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




def complete(request):
    User = Userinformation()
    try:
        User.user_name = 'sjy'
        User.user_name = request.POST.get('user_name')
        User.user_sex = request.POST.get('sex')
        User.user_email = request.POST.get('email')
        date = request.POST.get('date')
        User.user_hobby = request.POST.get('user_types')
        year = int(date.split(" ")[3])
        user_info = Registerinfo.objects.filter(user_name=User.user_name)
        user_info = list(user_info.values())
        User.user_account = user_info[0]['user_account']
        User.user_password = user_info[0]['user_password']
        User.user_phone = user_info[0]['user_phone']
        if year > 2022:
            User.user_age = 0
        else:
            User.user_age = 2022 - year
        print(User.user_name, User.user_sex, User.user_email, User.user_age, User.user_hobby)
        print(User.user_account, User.user_password, User.user_phone)
        User.save()


        response = {}
        information = find_Info(User.user_name)
        type_recommend = ""
        print(information, 11111)
        if information:
            type_recommend = type_movie_info(information['user_hobby'])

            response = {
                'code': 200,
                'message': "登录成功!",
                'userInfo': information,
                'type_recommend': type_recommend,
                'recommend': type_recommend,
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'code': 400, 'message': '用户信息读取失败，请重试!'})
    except:
        return JsonResponse({'code': 400, 'message': '请求失败！'})



def get_movie_info(request):
    surf = Surfinformation()
    try:
        movieID = request.POST.get('id')
        userID = request.POST.get('user_id')
        surf.surf_id = ''.join(random.choice(string.digits) for _ in range(3))
        surf.movie_id = movieID
        surf.user_id = userID
        surf.date_time = timezone.now()
        surf.link = ''.join(random.choice(string.ascii_letters) for _ in range(7))
        movies = Movieinformation.objects.filter(movie_id=movieID).values()
        if movies:
            movie = list(movies)
            styles = movie[0]["movie_style"][1:-1].replace("'", "").replace(" ", "").split(',')
            director = movie[0]["movie_director"][1:-1].replace("'", "").replace(" ", "").split(',')
            screenwriter = movie[0]["movie_screenwriter"][1:-1].replace("'", "").replace(" ", "").split(',')
            roles = movie[0]["movie_roles"][1:-1].replace("'", "").replace(" ", "").split(',')
            movie[0]['movie_style'] = "/".join(styles)
            movie[0]["movie_director"] = "/".join(director)
            movie[0]["movie_screenwriter"] = "/".join(screenwriter)
            movie[0]["movie_roles"] = "/".join(roles)

            name = movie[0].get('movie_name')

            comments = list(Moviecomments.objects.filter(movie_name=name).values())
            other_info = MovieInfo2.objects.filter(movie_name=name).exists()
            if other_info:
                other_info = list(MovieInfo2.objects.filter(movie_name=name).values())
                other_info[0]['star5'] = other_info[0]['star5'].replace("%", "")
                other_info[0]['star4'] = other_info[0]['star4'].replace("%", "")
                other_info[0]['star3'] = other_info[0]['star3'].replace("%", "")
                other_info[0]['star2'] = other_info[0]['star2'].replace("%", "")
                other_info[0]['star1'] = other_info[0]['star1'].replace("%", "")
                other_info1 = other_info[0]
            else:
                other_info1 = {
                    "person": "1235467人评价",
                    "star5": '47.3',
                    "star4": '33.3',
                    "star3": '11.3',
                    "star2": '4.0',
                    "star1": '4.1',
                    "good": '99.9%',
                    "introduction": "未获得电影简介！"
                }
            print(other_info1)
            surf.save()
            return JsonResponse({'code': 200, 'movie': movie[0], "comment": comments, "other_info": other_info1})
        else:
            return JsonResponse({'code': 400, 'message': '未找到电影信息！'})
    except:
        return JsonResponse({'code': 400, 'message': '请求失败！'})


def get_all_movie(request):
    try:
        type = request.POST.get('type')
        year = request.POST.get('year')
        region = request.POST.get('region')
        movies = Movieinformation.objects.all().values()
        print(type, year)
        item = []
        for movie in movies:
            styles = movie["movie_style"][1:-1].replace("'", "").replace(" ", "").split(',')
            director = movie["movie_director"][1:-1].replace("'", "").replace(" ", "").split(',')
            screenwriter = movie["movie_screenwriter"][1:-1].replace("'", "").replace(" ", "").split(',')
            roles = movie["movie_roles"][1:-1].replace("'", "").replace(" ", "").split(',')
            movie['movie_style'] = "/".join(styles)
            movie["movie_director"] = "/".join(director)
            movie["movie_screenwriter"] = "/".join(screenwriter)
            movie["movie_roles"] = "/".join(roles)
            if type in styles or type == "全部类型":
                if year == "全部年份" or year == movie['movie_year']:
                    if region == "全部地区" or region == movie["movie_country"]:
                        item.append(movie)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        return JsonResponse({"code": 200, "movies": item})
    except:
        return JsonResponse({"code": 404})


def get_movie(id):
    movie = Movieinformation.objects.filter(movie_id=id)
    movie = list(movie.values())
    director = movie[0]["movie_director"][1:-1].replace("'", "").replace(" ", "").split(',')
    roles = movie[0]["movie_roles"][1:-1].replace("'", "").replace(" ", "").split(',')
    movie[0]["movie_director"] = "/".join(director)
    movie[0]["movie_roles"] = "/".join(roles)
    return movie[0]

def get_record(request):
    try:
        account = request.POST.get('account')
        surf = Surfinformation.objects.filter(user_id=account).exists()
        if surf:
            surf = Surfinformation.objects.filter(user_id=account)
            surf_info = list(surf.values())
            i = 0
            for surf in surf_info:
                movie = get_movie(surf['movie_id'])
                surf_info[i]['movie_name'] = movie['movie_name']
                surf_info[i]['movie_director'] = movie['movie_director']
                surf_info[i]['movie_roles'] = movie['movie_roles']
                surf_info[i]['movie_evaluation'] = movie['movie_evaluation']
                i += 1
        else:
            surf_info = []
        favorite = Favoriteinformation.objects.filter(user=account).exists()
        if favorite:
            favorite = Favoriteinformation.objects.filter(user=account)
            favorite_info = list(favorite.values())
            i = 0
            for fav in favorite_info:
                movie = get_movie(fav['movie_id'])
                favorite_info[i]['movie_name'] = movie['movie_name']
                favorite_info[i]['movie_director'] = movie['movie_director']
                favorite_info[i]['movie_roles'] = movie['movie_roles']
                favorite_info[i]['movie_evaluation'] = movie['movie_evaluation']
                i += 1
        else:
            favorite_info = []
        return JsonResponse({
            "code": 200,
            "surf": surf_info,
            "favorite": favorite_info,
        })
    except:
        return JsonResponse({"code": 400, "surf": [], "favorite": []})



# def surf_movie(request):#用户浏览信息
#     print('------------------------------------------')
#     p3 = request.GET.get('p3')
#     print(p3)
#     uid = p3
#     # uid = 'OB324390'
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
#     return render(request, 'Surf_movie.html')
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
