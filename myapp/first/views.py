from django.shortcuts import render,redirect
from django.db import connection
from first import forms
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request,'start.html',{})

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


def logedin(request):
    
    if request.method == 'POST':
        form1  = forms.Dilogeform(request.POST)
        formpost = forms.Poster(request.POST)

        if form1.is_valid():
            x = form1.cleaned_data['Decision']
            if(str(x).upper() =='YES'):
                logout(request)
                return redirect('startap')
            else:
                print("DOne Task NOT Compleate")
                formobj = forms.Dilogeform()
                return render(request,'loginredirect.html',{'form':formobj})
        else :
            print("DOne Task NOT Compleate")
            formobj = forms.Dilogeform()
            return render(request,'loginredirect.html',{'form':formobj})
    else:
        formobj = forms.Dilogeform()
        formpost = forms.Poster()
        messages.success(request, 'Login successful as ')
        return render(request,'loginredirect.html',{'form':formobj,'formp':formpost})
