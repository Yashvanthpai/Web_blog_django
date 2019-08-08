from django.shortcuts import render,redirect,render_to_response
from django.db import connection
from first import forms
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
def post_data():
    query = 'select * from Blogs  WHERE post_date > DATEADD(day, -2, GetDate())'
    cur = connection.cursor()
    cur.execute(query)
    dic ={}
    li =['subject','date','content','file']
    count =1
    for x in cur.fetchall():
        temp={}
        for y in li:
            if y=='date':
                temp[y] = x[li.index(y)+2].strftime('%Y-%m-%d')
            else:
                temp[y]=x[li.index(y)+2]
        dic[count]=temp
        count+=1
    return dic

def index(request):
    val = post_data()
    return render(request,'start.html',{'data':val})

def logout_view(request):
    logout(request)
    return redirect('/')

def registration(request):
    if request.method == 'POST':
        form1  = forms.Userregistrtion(request.POST)
        form2 = forms.UserExtendedForm(request.POST ,request.FILES)

        if form1.is_valid():
            print("in file 1 save")
            form1.save()
            if form2.is_valid():
                print("in file 2 save")
                form2.save()
                myfile = request.FILES['myfile']
                fs = FileSystemStorage(location='static')
                filename = fs.save(myfile.name, myfile)
                print(myfile.name)
                return redirect('login')
            return render(request,'registratin.html',{'form':form1,'form1':form2})
        return render(request,'registratin.html',{'form':form1,'form1':form2})
    else:
        formobj = forms.Userregistrtion()
        formobj1 = forms.UserExtendedForm()
        return render(request,'registratin.html',{'form':formobj,'form1':formobj1})

def poster_serializer():
    querry = "Select * from Blogs"
    cur = connection.cursor()
    cur.execute(querry)
    dic ={}
    li =['username','subject','date','content','file']
    count =1
    for x in cur.fetchall():
        temp={}
        for y in li:
            if y=='date':
                temp[y] = x[li.index(y)+1].strftime('%Y-%m-%d')
            else:
                temp[y]=x[li.index(y)+1]
        dic[count]=temp
        count+=1
    return dic

@login_required
def logedin(request):
    val = poster_serializer()
    if request.method == 'POST':
        form1  = forms.Dilogeform(request.POST)
        formpost = forms.Poster(request.POST,request.FILES)

        if form1.is_valid():
            x = form1.cleaned_data['Decision']
            if(str(x).upper() =='YES'):
                logout(request)
                return redirect('startap')

        if formpost.is_valid() :
            myfile = request.FILES['image']
            fs = FileSystemStorage(location='static')
            filename = fs.save(myfile.name, myfile)
            try:
                formpost.save(myfile.name,request.user.get_username())
                return redirect('logedin')
            except Exception as exp:
                return render(request,'loginredirect.html',{'form':form1,'formp':formpost})
        else:
            return render(request,'loginredirect.html',{'form':form1,'formp':formpost})
    
    formobj = forms.Dilogeform()
    formpost = forms.Poster()
    messages.success(request, 'Login successful as ')
    return render(request,'loginredirect.html',{'form':formobj,'formp':formpost,'data':val})

@login_required
def mypost_view(request):
    return render(request,'myblog.html')