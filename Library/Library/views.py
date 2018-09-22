# -*- coding: utf-8 -*-  

from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
def index(request):
	context={}
	base.init(request,context)
	res=render(request,'index.html',context)
	return res
	
def Logout(request):
	res=redirect("/index/")
	print(request.GET["next"])
	res.delete_cookie("Username")
	try:
		del request.session["Username"]
	except Exception:
		pass
	return res
