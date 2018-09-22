# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member

def bemanager(request):

	context={}
	base.init(request,context)
	context['Err']=0
	context['Succ']=0
	fl=open('/home/Library/bemanager.log','a',encoding="utf-8")
	
	if (context['HaveLogin']==0):
		context['Err']=1
		context['ErrMsg']="请先登录"
		ret=render(request,"bemanager.html",context)
		fl.write(str(ontext))
		fl.write('\n')
		fl.close()
		return ret
	p=Member.objects.filter(name=context['Username'])[0]
	if (p.level==1):
		context['Err']=1
		context['ErrMsg']="你已经是管理员"
		ret=render(request,"bemanager.html",context)
		fl.write(str(context))
		fl.write('\n')
		fl.close()

		return ret
	if (request.method=='GET'):
		ret=render(request,'bemanager.html',context)
		return ret
	else:
		ID=request.POST['ID']
		if (len(ID)!=12):
			context['Err']=1
			context['ErrMsg']="序列号错误"
			fl.write(str(context))
			fl.write('\n')
			fl.close()

			ret=render(request,"bemanager.html",context)
			return ret
		for i in ID:
			if (i<'0' or i>'9'):
				context['Err']=1
				context['ErrMsg']="序列号错误"
				ret=render(request,"bemanager.html",context)
				fl.write(str(context))
				fl.write('\n')
				fl.close()

				return ret
		ID=int(ID)
		realID=0
		for i in range(0,len(p.password)):
			realID=(realID*233+(int(p.password[i])+37))%1000000000000
		context['realID']=realID
		print(realID)
		if (ID==realID):
			p.level=1;
			p.save()
			context['Succ']=1
			ret=render(request,"bemanager.html",context)
			fl.write(str(context))
			fl.write('\n')
			fl.close()

			return ret
		else:
			context['Err']=1
			context['ErrMsg']="序列号错误"
			ret=render(request,"bemanager.html",context)
			fl.write(str(context))
			fl.write('\n')
			fl.close()

			return ret
