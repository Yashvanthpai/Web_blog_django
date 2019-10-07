from django.conf.urls import url,include
from first import views
from django.contrib import admin
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView,PasswordChangeDoneView
urlpatterns=[
    url(r'login/$',LoginView.as_view(template_name="Registration/LoginView.html",extra_context={'passworreset':'false'}),name="login"),
    url(r'register/$',views.registration,name="register"),
    url(r'logout/$',views.logout_view,name="logout"),
    url(r'mypost/$',views.mypost_view,name='mypost'),
    url(r'^password_reset/$', PasswordResetView.as_view(template_name='Registration/password_reset_form.html'), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='Registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(template_name='Registration/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^password_reset/compleate$', LoginView.as_view(template_name='Registration/LoginView.html',extra_context={'passworreset':'false'}), name='password_reset_complete'),
    url(r'^password_change/$',PasswordChangeView.as_view(template_name='Registration/password_change_form.html',success_url='/logedin/'), name='password_change'),
    url(r'^logedin/$',views.logedin,name="logedin"),
    url(r'^like',views.likeview,name="like"),
    url(r'^comment',views.comment,name="comment"),
    url(r'^updatepost',views.updatepost_view,name="updatepost"),
    url(r'^$',views.index,name="startap"),

]
