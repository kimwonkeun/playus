"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from playus import views

app_name='playus'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    # path('test/',views.test,name='test'), #뭐지?????
    path('login/',views.login), #로그인시
    path('detail/<int:pk>/',views.detail,name='detail'), #놀이 상세보기
    path('changekakao',views.changekakao,name='changekakao'), #카카오채팅 바꾸기
    path('changenick',views.changenick,name='changenick'), #닉네임교체
    path('inputuser',views.inputuser,name='input'), # 유저 등록
    path('playus/<str:gpsX>/<str:gpsY>',views.playus,name='play'), # 놀이 만들기
    path('inputplaydata',views.inputplaydata), #놀이 등록
    path('partyin',views.partyin),
    path('inputgossip/<str:gossip>/<int:pk>',views.inputgossip),
    path('findbymap/<str:gpsX>/<str:gpsY>/<int:level>',views.findByMap,name='mapFind'),
    path('findbylist/<str:gpsX>/<str:gpsY>',views.findByList),
    path('userdetail/',views.userhome),
    #path('login/',include('login.urls')),
    path('inputUserdata/',views.inputuserdata),
    path('some',views.some),
]
