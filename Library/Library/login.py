# -*- coding: utf-8 -*-  

from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
@csrf_exempt
def Login(request):
	context={}
	if (request.method=='GET'):
		if ('next' in request.GET): context['next']=request.GET['next']
		else: context['next']='/index/'
		ret=render(request,'Login.html',context)
		return ret
	else:
		if ('next' in request.POST): context['next']=request.POST['next']
		else: context['next']='/index/'
		try:
			p=Member.objects.filter(name=request.POST["Username"])[0]
		except Exception:
			context["Err"]=1
			ret=render(request,"Login.html",context)
			return ret
			
		if (p.password==request.POST["Password"]):
			ret=redirect(context["next"])
			ret.set_cookie("Username",request.POST["Username"])
			request.session["Username"]=request.POST["Username"]
			return ret
		else:
			context["Err"]=1
			ret=render(request,"Login.html",context)
			return ret