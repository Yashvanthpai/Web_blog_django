from django.contrib.auth.models import User
from first.models import AuthUserExtended,AuthUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import connection
from datetime import datetime
from django.core import validators

uname=None


class Userregistrtion(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
    
    def save(self,commit=True):
        global uname
        uname = self.cleaned_data['username']
        user = super(Userregistrtion,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        print("In Save data user")
        
        if commit:
            user.save()
        
        return user


class  UserExtendedForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=[("male",'Male'),('female','Female')], required=True,widget=forms.RadioSelect)
    bdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'text','class': 'datepicker','autocomplete':"off"}),required=True)
    myfile = forms.FileField(label="Choose profile pic",required=False)

    class Meta:
        model = AuthUserExtended
        fields = ['gender','bdate','myfile']
    
    def save(self,commit=True):
        global uname
        sql ="insert into auth_user_extended values('"+str(uname)+"','"+str(self.cleaned_data['bdate'])+"','"+str(self.cleaned_data['gender'])+"');"
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        print("Hello")

class Poster(forms.Form):
    Subject = forms.CharField( label="Subject",max_length=120, required=True,help_text="Subject for Post")
    Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'text','class': 'datepicker','autocomplete':"off"}),required=True,initial=datetime.today())
    Post = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}) ,required=True,help_text="Content of post")
    image = forms.FileField(label="Choose pic",required=False)

    def save(self,arg1,arg2):
        try:
            sql ="insert into Blogs values('"+str(arg2)+"','"+str(self.cleaned_data['Subject'])+"','"+str(self.cleaned_data['Date'])+"','"+str(self.cleaned_data['Post'])+"','"+str(arg1)+"');"
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.close()
        except Exception as p:
            raise(forms.ValidationError("Validation Error"))


class Dilogeform(forms.Form):
    Decision = forms.ChoiceField(choices=[("yes",'YES'),('no','NO')], required=True,widget=forms.RadioSelect,initial={'yes':'YES'})

