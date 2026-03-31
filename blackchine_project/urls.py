"""blackchine_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from user import views as user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('^$',user_views.index,name="index"),
    url('user/register', user_views.register, name="register"),
    url('user/userpage', user_views.userpage, name="userpage"),
    url('user/viewdata', user_views.viewdata, name="viewdata"),
    url('^user/otppage/(?P<pk>\d+)/$', user_views.otppage, name="otppage"),
    url('download_page',user_views.download_page,name="download_page"),
    url('^user/secure_download/(?P<pk>\d+)/$', user_views.secure_download, name="secure_download"),
    url('graphical_page',user_views.graphical_page,name="graphical_page"),
    url('mydetail',user_views.mydetail,name="mydetail"),
    url('admin-login', user_views.admin_login, name="admin_login"),
    url('admin-logout', user_views.admin_logout, name="admin_logout"),
    url('admin-dashboard', user_views.admin_dashboard, name="admin_dashboard"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
