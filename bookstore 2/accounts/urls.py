from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView, name='login'),
    url(r'logout/$',views.LogoutView.as_view(), name='logout'),
    url(r'signUp/$',views.SignUpView.as_view(), name='signup'),
]