# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
def usermodify(request):
	context={}
	base.init(request,context)
	context['Err']=0
	context['Succ']=0
	if (context['HaveLogin']==0):
		context['Err']=1
		context['ErrMsg']="请先登录"
		ret=render(request,"usermodify.html",context)
		return ret
	if (request.method=='GET'):
		if ('next' in request.GET): context['next']=request.GET['next']
		else: context['next']='/index/'
		ret=render(request,'usermodify.html',context)
		return ret
	else:
		if ('next' in request.POST): context['next']=request.POST['next']
		else: context['next']='/index/'
	
	old_password=request.POST['old_password']
	p=Member.objects.filter(name=context['Username'])[0]
	if (p.password!=old_password):
		context['Err']=1
		context['ErrMsg']="密码错误"
		ret=render(request,"usermodify.html",context)
		return ret
	new_password=request.POST['new_password']
	re_password=request.POST['re_password']
	if (len(new_password)!=0 and (len(new_password)<6 or len(new_password)>15)):
		context['Err']=1
		context['ErrMsg']='密码长度必须为6至15位'
		ret=render(request,'usermodify.html',context)
		return ret
	if (new_password!=re_password):
		context['Err']=1
		context['ErrMsg']="两次输入密码不匹配"
		ret=render(request,'usermodify.html',context)
		return ret
	if (len(request.POST['realname'])>0 and (len(request.POST['realname'])<2 or len(request.POST['realname'])>15)):
		context['Err']=1
		context['ErrMsg']='真实姓名必须为二到十五个字符'
		ret=render(request,'usermodify.html',context)
		return ret	
	p.password=new_password
	p.realname=request.POST['realname']
	p.email=request.POST['email']
	if (len(request.POST['email'])>0): p.email=request.POST['email']
	p.save()
	context['Succ']=1
	ret=render(request,"usermodify.html",context)
	return ret