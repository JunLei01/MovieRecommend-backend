"""MovieRecommend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path,include
from MRApp import views
# from dj_test import views

urlpatterns = [
    path('login', views.Login),
    path('capture', views.get_images),
    path('register', views.RegisterView),
    path('complete', views.complete),
    path('face', views.set_face),

    path('all_movie', views.get_all_movie),
    path('movie_info', views.get_movie_info),
    path('get_record', views.get_record),
    # path('surf_movie', views.surf_movie),
]