from django import forms
from playus.models import player
from django.core.exceptions import ValidationError


class userInputForm(forms.ModelForm):
    class Meta:
        model = player
        fields = ['nickname','kakaochat']       

class playInputForm(forms.Form):    
    kakaochat=forms.CharField(help_text="카카오 챗에서 오픈 채팅을 열어주세요.")
    detail=forms.CharField()
    title=forms.CharField()
    def clean_renewal_kakaochat(self):
        kakaochat=self.cleaned_data['kakaochat']
        detail=self.cleaned_data['detail']
        title=self.cleaned_data['title']

        if kakaochat == '':
            raise ValidationError(_('카카오 챗을 넣지 않으셨네요..'))
        if detail=='':
            raise ValidationError(_('내용이 없음'))        
        if title=='':
            raise ValidationError(_('제목이 없음'))
            
        return kakaochat
    
    