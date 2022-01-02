from django.db import models
from django.db.models.fields import DateField
# Create your models here.

class player(models.Model):
    uniqueid = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    gender = models.CharField(max_length=5)
    kakaochat = models.CharField(max_length=50)
    level = models.SmallIntegerField()

    def __str__(self):
        return self.uniqueid

class userlogin(models.Model):
    userid = models.CharField(max_length=50)
    recentlog = models.DateField()
    recenpos = models.CharField(max_length=50)
    writetime = models.SmallIntegerField()
    player=models.ForeignKey(player,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.recenpos

class playerdetail(models.Model):
    player = models.ForeignKey(player,on_delete=models.CASCADE)
    birth = models.DateField()
    kakaoemail=models.CharField(max_length=100)
    realname=models.CharField(max_length=20)
    picture=models.FileField()

    def __str__(self):
        return self.realname
    

class playdata(models.Model):
    userid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    starttime = models.DateTimeField()
    gpsX = models.FloatField()    
    gpsY = models.FloatField()
    detail = models.TextField()
    kakaochat = models.CharField(max_length=50)
    zoneXY= models.CharField(max_length=10)
    zoneX=models.CharField(max_length=10)
    zoneY=models.CharField(max_length=10)
    party=models.SmallIntegerField()
    player=models.ForeignKey(player,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class partytable(models.Model):
    playdata=models.ForeignKey(playdata,on_delete=models.CASCADE)
    userid = models.CharField(max_length=50)
    partyindate = models.DateField()
    p_gender=models.CharField(max_length=5)
    p_nick=models.CharField(max_length=50)

    def __str__(self):
        return self.p_nick

class pdatagossip(models.Model):
    p_data=models.ForeignKey(playdata,on_delete=models.CASCADE)
    gossip=models.CharField(max_length=30)
    nickname=models.CharField(max_length=50)
    userid=models.CharField(max_length=50)




