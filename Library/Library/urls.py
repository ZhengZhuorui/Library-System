# -*- coding: utf-8 -*-  

"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from Library import views
from Library import login
from Library import register
from Library import search
from Library import newbook
from Library import book
from Library import ret
from Library import brw
from Library import bemanager
from Library import usermodify
from Library import status
from Library import comm
from Library import manageuser
from Library import rmbook
from Library import rebrw
from Library import FAQ

urlpatterns = [
    path('admin/', admin.site.urls),
	re_path(r'^$',views.index),
	re_path(r'^index/$',views.index),
	re_path(r'^Login/$',login.Login),
	re_path(r'^Logout/$',views.Logout),
	path('search/<int:nowpage>/',search.search),
	path('search/',search.search),
	re_path(r'^Register/$',register.Register),
	re_path(r'^newbook/$',newbook.newbook),
	path('book/<slug:isbp>/',book.book),
	path('book/<slug:isbp>/<int:cmpg>/',book.book),
	re_path(r'^return/$',ret.ret),
	re_path(r'^bemanager/$',bemanager.bemanager),
	re_path(r'^borrow/$',brw.brw),
	re_path(r'^usermodify/$',usermodify.usermodify),
	path('status/',status.status),
	path('status/<int:nowpage>/',status.status),
	path('rmbook/',rmbook.rmbook),
	path('comm/<slug:isbn>/<slug:cmpg>/',comm.comm),
	path('rebrw/',rebrw.rebrw),
	path('FAQ/',FAQ.FAQ),
	path('manageuser/',manageuser.manageuser),
]
