# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Book
from LibData.models import Borrow
def brw(request):
	context={}
	base.init(request,context)
	context['Err']=0
	context['Succ']=0
	if (request.method=='GET'):
		if ('isbn' in request.GET): context['isbn']=request.GET['isbn']
		else: context['isbn']=""
		ret=render(request,'borrow.html',context)
		return ret
	else:
		if (context['HaveLogin']==0):
			context['Err']=1
			context['ErrMsg']="请先登录"
			ret=render(request,"borrow.html",context)
			return ret
		context['isbn']=request.POST['isbn']
		m=Member.objects.filter(name=context['Username'])[0]
		try:
			b=Book.objects.filter(isbn=context['isbn'])[0]
		except Exception:
			context['Err']=1
			context['ErrMsg']="该书不存在"
			ret=render(request,"borrow.html",context)
			return ret
		if (m.bownum>=5):
			context['Err']=1
			context['ErrMsg']="你的借阅数已达上限"
			ret=render(request,"borrow.html",context)
			return ret
		if (m.level==-1):
			context['Err']=1
			context['ErrMsg']="你已进入黑名单，请联系管理员"
			ret=render(request,"borrow.html",context)
			return ret
		if (m.level==1):
			context['Err']=1
			context['ErrMsg']="你是管理员，不能借阅"
			ret=render(request,"borrow.html",context)
			return ret
			
		if (b.left<=0):
			context['Err']=1
			context['ErrMsg']="该书已全被借阅"
			ret=render(request,"borrow.html",context)
			return ret
		try:
			q=Borrow.objects.filter(user=m.name,bookisbn=b.isbn,status__gte=1)[0]
			context['Err']=1
			context['ErrMsg']="你已借阅该书"
			ret=render(request,"borrow.html",context)
			return ret
		except Exception:
			pass
		
		m.bownum+=1
		b.left-=1
		b.borrownum+=1
		p=Borrow(user=m,bookisbn=b,status=1)
		p.save()
		b.save()
		m.save()
		context['Succ']=1
		ret=render(request,"borrow.html",context)
		return ret
