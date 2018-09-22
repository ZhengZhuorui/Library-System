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

def rebrw(request):
	context={}
	base.init(request,context)
	context['Err']=0
	context['Succ']=0
	if (request.method=='GET'):
		if ('isbn' in request.GET): context['isbn']=request.GET['isbn']
		else: context['isbn']=""
		if ('name' in request.GET): context['name']=request.GET['name']
		else: context['name']=""
		ret=render(request,'rebrw.html',context)
		return ret
	else:
		if (context['HaveLogin']==0):
			context['Err']=1
			context['ErrMsg']="请先登录"
			ret=render(request,"return.html",context)
			return ret
		context['isbn']=request.POST['isbn']
		
		
		m=Member.objects.get(name=context['Username'])
		try:
			b=Book.objects.get(isbn=context['isbn'])
		except Exception:
			context['Err']=1
			context['ErrMsg']="该书不存在"
			ret=render(request,"return.html",context)
			return ret
		
		try:
			p=Borrow.objects.get(user=m,bookisbn=b,status=1)
		except Exception:
			context['Err']=1
			context['ErrMsg']="你没有借阅过该书或者已续借过"
			ret=render(request,"return.html",context)
			return ret
		
		p.status=2
		#print(time.strftime("%Y-%m-%d", time.localtime()))
		p.save()
		
		
		context['Succ']=1
		ret=render(request,"rebrw.html",context)
		return ret