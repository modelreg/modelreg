"""modelreg URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/',    admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^profile/qrcode.png',  views.profile_qrcode_img, name='profile_code'),
    url(r'^profile/edit',        views.profile, name='profile'),

    url(r'^c/(?P<ident>[\w\d]+)', views.case_finder, name='case_finder'),
    url(r'^oc/(?P<pk>\d+)',  views.case_owner, name='case_owner'),

    url(r'^f/(?P<ident>[\w\d]+)\.(?P<auth>[\w\d]+)',  views.found, name='found'),
    url(r'^found/',  views.found_info, name='found_info'),
    url(r'^$',  views.index),
]
