# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Book
@csrf_exempt
def rmbook(request):
	context={}
	base.init(request,context)
	context["Err"]=0
	context['Succ']=0
	if (context['HaveLogin']!=1):
		context['Err']=1
		context['ErrMsg']="请先登录"
		ret=render(request,'rmbook.html',context)
		return ret
	m=Member.objects.get(name=context['Username'])
	if (m.level!=1):
		context['Err']=1
		context['ErrMsg']="需要管理员权限"
		ret=render(request,'rmbook.html',context)
		return ret
	if (request.method=='GET'):
		if ('isbn'in request.GET): context['isbn']=request.GET['isbn']
		ret=render(request,'rmbook.html',context)
		return ret
	else:
		#try:
		if (1):
			context['isbn']=request.POST['isbn']
			isbn=request.POST['isbn']
			print(isbn)
			try:
				p=Book.objects.get(isbn=isbn)
			except Exception as e:
				print(e)
				context['Err']=1
				context['ErrMsg']="该书不存在"
				ret=render(request,'rmbook.html',context)
				return ret
			if (p.left!=p.number):
				context['Err']=1
				context['ErrMsg']="有部分图书未归还，无法移除"
				ret=render(request,'rmbook.html',context)
				return ret
			p.left=p.number=0
			p.save()
			context['Succ']=1
			ret=render(request,"rmbook.html",context)
			return ret