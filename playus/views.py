from datetime import time
from django.http.request import HttpRequest
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render
from .models import *
from django.utils import timezone
from datetime import datetime
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from playus.forms import userInputForm,playInputForm
import requests
import json
# Create your views here.
def index(request):
    date=datetime.now()
    return HttpResponse(date)

# def test(request):
#     return render(request,'inputUser.html',{'uid':'7',})
@csrf_exempt
def login(request):
    try: 
        address=request.POST['address']
        app=request.POST['app']
        uid=request.POST['uid']       
        ServerApp=("5e237e06","3ceae297","3cff30d8","e6909cf0","7b3d6739","d8932aac","278fa541") #서버쪽 판단 서버가 앱인지 아닌지 암구호로 판단
        ServerappOrnot=ServerApp[datetime.today().weekday()]   
        # return HttpResponse(ServerappOrnot)     
        #+":"+ServerApp[datetime.today().weekday()]
        if app==ServerappOrnot : #앱에서만 접속가능
            request.session['uid']=uid #세션 생성            
            # return HttpResponse(request.session['uid'])
            playerdata=player.objects.get(uniqueid=uid)
            if playerdata.level > 3 :
                return redirect('/some?address='+address+'&clickuser') #글쓰기 권한설정
            else :
                return redirect('/some?address='+address) #글쓰기 권한설정

    except player.DoesNotExist:       
        return render(request,'inputUser.html')

def some(request):
    address=request.GET.get('address')
    uid=request.session['uid']
    playerdata=player.objects.get(uniqueid=uid)
    p_data=playdata.objects.filter(userid=uid,starttime__gt=timezone.now()).order_by('starttime')              
    inplay_data=playdata.objects.raw('select playus_playdata.id,title,starttime,detail from playus_playdata,playus_partytable where playus_playdata.id = playus_partytable.playdata_id and playus_partytable.userid="%s" and playus_playdata.starttime > "%s" order by starttime' % (uid,timezone.now()))
    context={
            'playerdata':playerdata,
            'p_data':p_data,
            'uid':uid,
            'inplay_data':inplay_data,
            }
            # 유저 데이타 로그인 기록.. 
    lognow=userlogin.objects.filter(userid=uid,recentlog=datetime.today()) #로그인시 로그인 장소와 위치 기록
    if lognow.count() == 0:
        loginData=userlogin()
        loginData.player=player.objects.get(uniqueid=uid)
        loginData.userid=uid
        loginData.recentlog=datetime.today()
        loginData.recenpos=address
        loginData.writetime = 1        
        loginData.save()
    else:
        logupdate=userlogin.objects.get(userid=uid,recentlog=datetime.today())
        logupdate.recenpos=address
        logupdate.save()
                           
    return render(request,'playhome.html',context)

    

def detail(request,pk):
    if request.session['uid']:
        try:
            p_data=playdata.objects.get(id=pk)        
            partyindata=partytable.objects.filter(playdata=p_data)
            gossipdata=pdatagossip.objects.filter(p_data=p_data)
            uid=request.session['uid']      
            playerdata=player.objects.get(uniqueid=uid)
            show=1
            for outdata in partyindata: #참석했는지 여부 파악
                if outdata.userid == uid:
                    show=0           

            context={
                'playdata':p_data,
                'partydata':partyindata,
                'gossipdata':gossipdata,
                'nick':playerdata.nickname,
                'gender':playerdata.gender,
                'userid':uid,
                'playdata':p_data,
                'show':show,
            }
            return render(request,"playdetail.html",context)
        except player.DoesNotExist:
            return HttpResponse('no user')
    else:
        return HttpResponse("앱으로 재접속해 주십시요")

def changekakao(request):
    try:        
        # if 'uid' not in request.COOKIES:
        uid=request.session['uid']      
        change=player.objects.get(uniqueid=uid)
        change.kakaochat=request.GET.get('kakaochat')
        change.save()
        p_data=playdata.objects.filter(userid=uid)
        context={
            'outdata':change,
            'p_data':p_data,
            'uid':uid,
        }
        return render(request,'inputuserdata.html',context)
    except player.DoesNotExist:              
        return HttpResponse("앱으로 재접속해 주십시요")

def changenick(request):
    try:        
        # if 'uid' not in request.COOKIES:
        uid=request.session['uid']      
        change=player.objects.get(uniqueid=uid)
        change.nickname=request.GET.get('nickname')
        change.save()
        p_data=playdata.objects.filter(userid=uid)
        context={
            'outdata':change,
            'p_data':p_data,
            'uid':uid,
        }
        return render(request,'inputuserdata.html',context)
    except player.DoesNotExist:              
        return HttpResponse("앱으로 재접속해 주십시요")


def inputuser(request):
    uid=request.session['uid'] #앱 접속만 허용
    if uid:
        if request.method == 'POST':
            form = userInputForm(request.POST)
            if form.is_valid():
                nick=request.POST['nickname']            
                gen=request.POST['inlineRadioOptions']
                kakao=request.POST['kakaochat']
                level=1; #기본레벨 마이너스 레벨은 사용금지 유저
                new_user=player(uniqueid=uid,nickname=nick,gender=gen,kakaochat=kakao,level=level)
                # return HttpResponse()
                new_user.save()
                p_data=playdata.objects.filter(userid=uid)
                context={
                    'playerdata':new_user,
                    'p_data':p_data,
                    'uid':uid,
                }        
                return render(request,'playhome.html',context)
            else:
                form=userInputForm()
                return render(request,'inputUser.html',{'form':form,'uid':uid})
        else:
            form=userInputForm()
            return render(request,'inputUser.html',{'form':form,'uid':uid})
    else:
        return HttpResponse("앱으로 재접속해 주십시요")

        
def playus(request,gpsX,gpsY): #놀이데이타 생성
    uid=request.session['uid']
    if uid:
        try:                
            playerdata=player.objects.get(uniqueid=uid)
            context={
                'gpsX':gpsX,
                'gpsY':gpsY,
                'playerdata':playerdata,
                }
            return render(request,'inputData.html',context)
        except player.DoesNotExist:
            return HttpResponse('앱으로 재접속해 주십시요')
    else:
        return HttpResponse('앱으로 접속해 주세요')

def inputplaydata(request): #놀이데이타 저장
    uid=request.session['uid']
    if  uid:
        if request.method == 'POST':
            form = playInputForm(request.POST)
            if form.is_valid():
                inputplayData=playdata()        
                inputplayData.player=player.objects.get(uniqueid=uid)
                inputplayData.title=request.POST['title']
                inputplayData.userid=request.POST['uniqueid']
                inputplayData.gpsX=request.POST['gpsX']
                inputplayData.gpsY=request.POST['gpsY']
                gpsX=request.POST['gpsX']
                gpsY=request.POST['gpsY']
                inputplayData.starttime=request.POST['startdate']
                inputplayData.detail=request.POST['detail']
                inputplayData.kakaochat=request.POST['kakaochat'] 
                inputplayData.zoneX=str(int(float(gpsX)))+str(int(float(gpsY))) #변경 level1
                inputplayData.zoneY=str(int(float(gpsX)*10))+str(int(float(gpsY)*10)) #변경 level2
                inputplayData.zoneXY=str(int(float(gpsX)*100))+str(int(float(gpsY)*100)) #변경 level3
                inputplayData.party=10
                inputplayData.save()
                return render(request,'savesucess.html')
            else:                
                form=playInputForm()
                return render(request,'inputData.html',{'form':form,'uid':uid})
    else:
        return HttpResponse("앱으로 접속해 주세요")

def partyin(request):
    uid=request.session['uid']
    if uid:
        if request.method == 'POST':
            inputpartyin=partytable()
            inputpartyin.playdata=playdata.objects.get(id=request.POST['playdata_id'])
            inputpartyin.userid=request.POST['userid']
            inputpartyin.p_gender=request.POST['gender']
            inputpartyin.p_nick=request.POST['nick']
            inputpartyin.partyindate=datetime.today()
            inputpartyin.save()

            p_data=playdata.objects.get(id=request.POST['playdata_id'])
            partyindata=partytable.objects.filter(playdata=p_data)
            gossipdata=pdatagossip.objects.filter(p_data=p_data)
        
            playerdata=player.objects.get(uniqueid=uid)
            context={
                'playdata':p_data,
                'partydata':partyindata,
                'gossipdata':gossipdata,
                'nick':playerdata.nickname,
                'gender':playerdata.gender,
                'userid':uid,
                'playdata':p_data,
            }
            return render(request,"playdetail.html",context)
        else:
            return HttpResponse('앱으로 접속해 주세요')
    else:
        return HttpResponse('앱으로 접속해 주세요')

def inputgossip(request,gossip,pk):
    try:
        uid=request.session['uid']
        playerdata=player.objects.get(uniqueid=uid)
        #잡담 저장구문
        inputgossip=pdatagossip()
        inputgossip.p_data=playdata.objects.get(id=pk)
        inputgossip.gossip=gossip
        inputgossip.nickname=playerdata.nickname
        inputgossip.userid=uid
        inputgossip.save() # 잡담이 저장되는 구문        
        print(gossip)
        context={
            'gossip':gossip,
            'nickname':playerdata.nickname,            
        }
        return JsonResponse(context) 
    except player.DoesNotExist:
        return HttpResponse('앱으로 재접속해 주세요')

def findByMap(request,gpsX,gpsY,level):
    if level < 6:
        findZoneXY=str(int(float(gpsX)*100))+str(int(float(gpsY)*100))
        outdata=playdata.objects.filter(zoneXY=findZoneXY,starttime__gt=timezone.now())
    elif level >= 6 and level < 10:
        findZoneXY=str(int(float(gpsX)*10))+str(int(float(gpsY)*10))
        outdata=playdata.objects.filter(zoneY=findZoneXY,starttime__gt=timezone.now())
    else:
        findZoneXY=str(int(float(gpsX)))+str(int(float(gpsY)))
        outdata=playdata.objects.filter(zoneX=findZoneXY,starttime__gt=timezone.now())
    
    context={
        'playdata':outdata,
        'gpsX':gpsX,
        'gpsY':gpsY,
        'maplevel':level,
    }
    return render(request,'map.html',context)

def findByList(request,gpsX,gpsY):
    try:
        gpsX=float(gpsX)
        gpsY=float(gpsY)            
        # inplay_data=playdata.objects.raw('select abs(gpsX-%f)+abs(gpsY-%f) as gpsXY, from playus_playdata where playus_playdata.starttime > "%s" order by gpsXY' % (gpsX,gpsY,timezone.now()))
        inplay_data=playdata.objects.raw('select abs(gpsX-%f)+abs(gpsY-%f) as outXY,title,id,starttime,detail from playus_playdata where playus_playdata.starttime > "%s" order by outXY limit 20' % (gpsX,gpsY,timezone.now()))
        context={
        'outputTable':inplay_data,
        'gpsX':gpsX,
        'gpsY':gpsY,
        }
        return render(request,'playlist.html',context)
    
    except playdata.DoesNotExist:
        return HttpResponse('자료 없음')

def userhome(request):
    uid=request.session['uid']
    playerdata=player.objects.get(uniqueid=uid)                
    p_data=playdata.objects.filter(userid=uid,starttime__gt=timezone.now()).order_by('starttime')              
    inplay_data=playdata.objects.raw('select playus_playdata.id,title,starttime,detail from playus_playdata,playus_partytable where playus_playdata.id = playus_partytable.playdata_id and playus_partytable.userid="%s" and playus_playdata.starttime > "%s" order by starttime' % (uid,timezone.now()))
        #inplay_data=playdata.objects.all()
        #세션 생성
    context={
       'playerdata':playerdata,
       'p_data':p_data,
       'uid':uid,
       'inplay_data':inplay_data,
        }
    return render(request,'playhome.html',context)

def inputuserdata(request):
    uid=request.session['uid'] 
    playerdata=player.objects.get(uniqueid=uid)
    context={
        'outdata':playerdata,
    }
    return render(request,"inputuserdata.html",context)

def oauth(request):
    code=request.GET['code']
    client_id='68c1537331b0409bb25b523b593af181'
    redirect_uri='http://152.67.213.106/oauth'
    access_token_uri="https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    
    access_token_uri +="client_id="+client_id
    access_token_uri +="&redirect_uri="+redirect_uri
    access_token_uri +="&code="+code

    access_token_uri_data=requests.get(access_token_uri)
    json_data=access_token_uri_data.json()
    access_token=json_data['access_token']  
    user_profile_info_uri="https://kapi.kakao.com/v2/user/me?access_token="  
    user_profile_info_uri+=str(access_token)

    user_profile_info_data=requests.get(user_profile_info_uri)
    user_json_data=user_profile_info_data.json()
    user_email = user_json_data['kakao_account']['email']
    return redirect('inuserdata')

def kakao_login(request):
    login_uri='https://kauth.kakao.com/oauth/authorize?'
    client_id='68c1537331b0409bb25b523b593af181'
    redirect_uri='http://152.67.213.106/oauth'
    login_uri +='client_id='+ client_id
    login_uri +='&redirect_uri='+redirect_uri
    login_uri +='&response_type=code&scope=account_email'
    return redirect(login_uri)