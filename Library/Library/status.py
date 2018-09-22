# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Borrow

def status(request,nowpage=1):
	context={}
	base.init(request,context)
	cursor = connection.cursor()
	context['level']=0
	tmp=0
	whereQ=""
	query="select * from LibData_borrow "
	try:
		p=Member.objects.get(name=context['Username'])
		context['level']=p.level
	except Exception:
		pass
		
	if ('user' in request.GET):	context["user"]=request.GET['user']
	if ('isbn' in request.GET):context["isbn"]=request.GET['isbn']
	if ('st_date' in request.GET):context["st_date"]=request.GET['st_date']
	if ('en_date' in request.GET):context["en_date"]=request.GET['en_date']
	if ('stat' in request.GET):context["stat"]=request.GET['stat']

	if (context['level']!=1): 
		if (tmp==1):whereQ+=" and  "
		whereQ+="user_id='"+context['Username']+"'"
		tmp=1
	elif (('user' in request.GET) and len(request.GET['user'])>0):
		if (tmp==1):whereQ+=" and "
		whereQ+=" user_id='"+request.GET['user']+"'"
		tmp=1
	if (('isbn' in request.GET) and len(request.GET['isbn'])>0):
		if (tmp==1):whereQ+=" and  "
		whereQ+="bookisbn_id='"+request.GET['isbn']+"'"
		tmp=1
	
	if (('st_date' in request.GET) and len(request.GET['st_date'])>0):
		if (tmp==1):whereQ+=" and  "
		whereQ+=" st_date>='"+request.GET['st_date']+"'"
		tmp=1
	if (('en_date' in request.GET) and len(request.GET['en_date'])>0):
		if (tmp==1):whereQ+=" and  "
		whereQ+=" st_date<='"+request.GET['en_date']+"'"
		tmp=1
		
	if (('stat' in request.GET) and len(request.GET['stat'])>0 and request.GET['stat']!='3'):
		if (tmp==1):whereQ+=" and  "
		whereQ+="status="+request.GET['stat']
		tmp=1
	
	print(whereQ)
	if (tmp!=0): query+=" where "+whereQ
	query+=" order by st_date desc"
	print(query)
	brw_list=()
	try:
		cursor.execute(query)
		brw_list=cursor.fetchall()
	except Exception:
		pass
		
	#print(brw_list)
	if (len(brw_list)%30==0): pagenum=int(len(brw_list)/30)
	else: pagenum=int(len(brw_list)/30+1)
	
	rbrw_list=[]
	for i in brw_list:
		x={'rbw':0,'con':i}
		if (i[4]==1 and p.bownum<=5 and p.level==0):x['rbw']=1
		rbrw_list.append(x)
	
	#print(pagenum)
	context['pagepre']=False if (nowpage<=1) else True
	context['pagenext']=False if (nowpage>=pagenum) else True
	context['pagep']=nowpage-1
	context['pagen']=nowpage+1
	pages=[]
	for i in range(1,pagenum+1):
		if (i==nowpage):pages.append(i)
		else:pages.append(i)
	print(pages)
	context['pages']=pages
	brws=[]
	for i in range((nowpage-1)*30,nowpage*30): 
		try:
			brws.append(rbrw_list[i])
		except Exception:
			pass
	print(brws)
	context["brws"]=brws
	res=render(request,'status.html',context)
	return res
