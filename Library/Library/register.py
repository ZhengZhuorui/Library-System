# -*- coding: utf-8 -*-  

from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
@csrf_exempt
def Register(request):
	context={}
	base.init(request,context)
	context['Err']=0
	context['Succ']=0
	if (request.method=='GET'):
		ret=render(request,'Register.html',context)
		return ret
	else:
		context['Err']=0
		try:
			p=Member.objects.filter(name=request.POST['Username'])[0]
			context['Err']=1
			context['ErrMsg']='用户名已被注册'
			ret=render(request,'Register.html',context)
			return ret
		except Exception:
			pass
		
		if (len(request.POST['Username'])<2 or len(request.POST['Username'])>15):
			context['Err']=1
			context['ErrMsg']='用户名必须为二到十五个字符'
			ret=render(request,'Register.html',context)
			return ret
			
		if (len(request.POST['Realname'])<2 or len(request.POST['Realname'])>15):
			context['Err']=1
			context['ErrMsg']='真实姓名必须为二到十五个字符'
			ret=render(request,'Register.html',context)
			return ret
		if (len(request.POST['Password'])<6 or len(request.POST['Password'])>15):
			context['Err']=1
			context['ErrMsg']='密码长度必须为6至15位'
			ret=render(request,'Register.html',context)
			return ret
			
		if (request.POST['Password']!=request.POST['RePassword']):
			context['Err']=1
			context['ErrMsg']="两次输入密码不匹配"
			ret=render(request,'Register.html',context)
			return ret
			
		if (len(request.POST['Email'])==0):
			context['Err']=1
			context['ErrMsg']='请输入电子邮箱'
			ret=render(request,'Register.html',context)
			return ret
		try:
			fp=Member.objects.get(email=request.POST['Email'])
			context['Err']=1
			context['ErrMsg']='该邮箱已注册'
			ret=render(request,'Register.html',context)
			return ret
		except Exception:
			pass
		q=Member(name=request.POST['Username'],realname=request.POST['Realname'],password=request.POST['Password'],level=0,email=request.POST['Email'],bownum=0,readbook=0)
		q.save()
		context['Succ']=1
		ret=render(request,'Register.html',context)
		return ret
