# -*- coding: utf-8 -*-  

from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from LibData.models import Member
from LibData.models import Borrow
import datetime
def HaveLogin(request):
	if ("Username" in request.COOKIES):
		if (request.COOKIES["Username"]==request.session["Username"]):
			return 1
	return 0
	
def init(request,context):
	context["HaveLogin"]=HaveLogin(request)
	if (context["HaveLogin"]==1):
		context["Username"]=request.COOKIES["Username"]
		p=Member.objects.filter(name=request.COOKIES["Username"])[0]
		context["level"]=p.level
		print(context['level'])
		context['stat']=0
		now=datetime.datetime.now()
		try:
			b=Borrow.objects.filter(user=p,status__gte=1)
			x=y=0
			for i in b:
				if (((now.date()-i.st_date).days>=90 and i.status==1) or ((now.date()-i.st_date).days>=150 and i.status==2)):x+=1
				elif  (((now.date()-i.st_date).days>=75 and i.status==1) or ((now.date()-i.st_date).days>=135 and i.status==2)):y+=1
			if (x>0):
				p.level=-1
				p.save()
				context['stat']=2
				context['statnum']=x
			elif (y>0):
				context['stat']=1
				context['statnum']=y
		except Exception as e:
			print(e)
			pass
		print(context)