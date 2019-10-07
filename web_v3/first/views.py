from django.shortcuts import render,redirect,render_to_response,HttpResponse
from django.db import connection
from first import forms
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import datetime
import json

# Create your views here.
def post_data():
    query = 'select * from Blogs  WHERE post_date > current_date-4 order by post_date DESC'
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
                myfile = request.FILES['myfile']
                fs = FileSystemStorage(location='static')
                filename = fs.save(myfile.name, myfile)
                form2.save(Filename=myfile.name or None)
                return redirect('login')
            return render(request,'registratin.html',{'form':form1,'form1':form2})
        return render(request,'registratin.html',{'form':form1,'form1':form2})
    else:
        formobj = forms.Userregistrtion()
        formobj1 = forms.UserExtendedForm()
        return render(request,'registratin.html',{'form':formobj,'form1':formobj1})

def poster_serializer(uid,sql):
    cur = connection.cursor()
    cur.execute(sql)
    dic ={}
    li =['blogid','username','subject','date','content','file']
    count =1
    for x in cur.fetchall():
        temp={}
        for y in li:
            if y=='date':
                temp[y] = x[li.index(y)].strftime('%Y-%m-%d')
            elif y=='username':
                cur.execute("select username from auth_user where id="+str(x[li.index(y)]))
                temp[y]=cur.fetchall()[0][0]
            else:
                temp[y]=x[li.index(y)]
        sqlquery = "select * from bloglike where blogid="+str(x[0])+" and "+str(uid)+"= any(likes);"
        cur.execute(sqlquery)
        if cur.rowcount >0 :
            temp['like']="True"
        else:
            temp['like']='False'
        dic[count]=temp
        count+=1
    return dic

@login_required
def logedin(request):
    sql = "select * from Blogs order by post_date DESC;"
    val = poster_serializer(request.user.id,sql)
    formobj = forms.Dilogeform()
    messages.success(request, 'Login successful as ')
    return render(request,'loginredirect.html',{'data':val})



def likeview(request):
    if request.method =="POST" and request.is_ajax():
        x =  request.POST.get('operation')
        sqluerry = ""
        if x == 'update':
            sqluerry = "update bloglike set likes = array_append(likes,"+str(request.user.id)+") where blogid="+request.POST.get('blogid')+";"
        else:
            sqluerry = "update bloglike set likes = array_remove(likes,"+str(request.user.id)+") where blogid="+request.POST.get('blogid')+";"
        
        cur = connection.cursor()
        cur.execute(sqluerry)
        cur.close()
        return HttpResponse(None)
    return HttpResponse(None)

def comment(request):
    if request.method =="POST" and request.is_ajax():
        try:
            sql_queer = "select usernmae,cmt from blogcomment where blogid='"+str(request.POST.get('blogid'))+"';"
            cur = connection.cursor()
            cur.execute(sql_queer)
            x =cur.fetchall()
            data = json.dumps({'value':x})
            cur.close()
            return HttpResponse(data, content_type="application/json")
        except Exception as p:
            print(p)

    return HttpResponse(None)




@login_required
def mypost_view(request):
    if request.method == "POST":
        formpost = forms.Poster(request.POST,request.FILES)
        if formpost.is_valid() :
            print("In save of image")
            myfile = request.FILES['imgfile']
            fs = FileSystemStorage(location='static')
            filename = fs.save(myfile.name, myfile)
            try:
                formpost.save(myfile.name,request.user.id)
                return redirect('mypost')
            except Exception as exp:
                print(str(exp))
                return render(request,'myblog.html',{'formp':formpost,'exception':str(exp)})

    sql = "select * from blogs where userid='"+str(request.user.id)+"' order by post_date DESC;"
    val = poster_serializer(request.user.id,sql)
    formpost = forms.Poster()
    return render(request,'myblog.html',{'formp':formpost,'data':val,'exception':"None"})

def updatepost_view(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            sql =""
            if str(request.POST.get('option')) == 'update':
                    value = str(request.POST.get('values[body]')).strip()
                    sql = "update Blogs set tittle='"+str(request.POST.get('values[title]'))+"',post_date='"+str(request.POST.get('values[post_date]'))+"',body='"+value+"' where blogid='"+str(request.POST.get('values[blogid]'))+"';"
            else:
                  sql = "delete from Blogs where blogid='"+str(request.POST.get('values[blogid]'))+"';"
            print(sql)
            cur = connection.cursor()
            cur.execute(sql)
            cur.close()
            return HttpResponse(None)
        except Exception as p:
            return HttpResponse(str(p),status=401)
    return HttpResponse(None)