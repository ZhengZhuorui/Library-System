# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Book
from LibData.models import Borrow
import time

def ret(request):
	context={}
	base.init(request,context)
	context['Err']=0
	context['Succ']=0
	if (request.method=='GET'):
		if ('isbn' in request.GET): context['isbn']=request.GET['isbn']
		else: context['isbn']=""
		if ('name' in request.GET): context['name']=request.GET['name']
		else: context['name']=""
		ret=render(request,'return.html',context)
		return ret
	else:
		if (context['HaveLogin']==0):
			context['Err']=1
			context['ErrMsg']="请先登录"
			ret=render(request,"return.html",context)
			return ret
		context['isbn']=request.POST['isbn']
		context['name']=request.POST['name']
		
		
		root=Member.objects.filter(name=context['Username'])[0]
		if (root.level!=1):
			context['Err']=1
			context['ErrMsg']="你没有管理员权限"
			ret=render(request,"return.html",context)
			return ret
		m=Member.objects.filter(name=request.POST["name"])[0]
		try:
			b=Book.objects.filter(isbn=context['isbn'])[0]
		except Exception:
			context['Err']=1
			context['ErrMsg']="该书不存在"
			ret=render(request,"return.html",context)
			return ret
		
		try:
			p=Borrow.objects.filter(user=m,bookisbn=b,status__gte=1)[0]
		except Exception:
			context['Err']=1
			context['ErrMsg']="该用户没有借阅过该书"
			ret=render(request,"return.html",context)
			return ret
		
		m.bownum-=1
		b.left+=1
		p.status=0
		#print(time.strftime("%Y-%m-%d", time.localtime()))
		p.en_date=str(time.strftime("%Y-%m-%d", time.localtime()) )
		p.save()
		b.save()
		m.save()
		context['Succ']=1
		ret=render(request,"return.html",context)
		return ret
