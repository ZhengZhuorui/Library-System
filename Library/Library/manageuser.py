# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Book
@csrf_exempt
def manageuser(request):
	context={}
	base.init(request,context)
	context["Err"]=0
	context['Succ']=0
	if (context['HaveLogin']!=1):
		context['Err']=1
		context['ErrMsg']="请先登录"
		ret=render(request,'manageuser.html',context)
		return ret
	context["name"]=""
	root=Member.objects.get(name=context['Username'])
	if (root.level!=1):
		context['Err']=1
		context['ErrMsg']="你不是管理员"
		ret=render(request,'manageuser.html',context)
		return ret
	if (request.method=='GET'):
		if ('name' in request.GET):context['name']=request.GET['name']	
		ret=render(request,'manageuser.html',context)
		return ret
	else:
		if ('name' in request.POST):context['name']=request.POST['name']	
		print()
		try:
			m=Member.objects.get(name=context['name'])
		except Exception:
			context['Err']=1
			context['ErrMsg']="没有该用户"
			ret=render(request,'manageuser.html',context)
			return ret
		if (int(request.POST['level'])>=-1 and int(request.POST['level'])<=0):
			m.level=int(request.POST['level'])
			m.save()
			context['Succ']=1
			ret=render(request,"manageuser.html",context)
			return ret
		else:
			context['Err']=1
			context['ErrMsg']="权限修改错误"
			ret=render(request,'manageuser.html',context)
			return ret