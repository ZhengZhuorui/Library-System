# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
	
def insert(query,key,request,tmp):
	if ((key in request.GET) and (len(request.GET[key])>0)):
		if (tmp==1):query+=" and "
		query+=" "+key+'="'+request.GET[key]+'"'
		tmp=1
	return (query,tmp)
	
def search(request,nowpage=1):
	opbk=8
	
	context={}
	base.init(request,context)
	cursor = connection.cursor()
	query="select * from LibData_book "
	whereQ=""
	tmp=0
	query_list=("isbn","publisher","language")
	for q in query_list:
		(whereQ,tmp)=insert(whereQ,q,request,tmp)
	
	if (("name" in request.GET) and len(request.GET['name'])>0):
		if (tmp==1):whereQ+=" and "
		whereQ+=" name like '%"+request.GET['name']+"%' "
		tmp=1
	if ('isbn' in request.GET):	context["isbn"]=request.GET['isbn']
	if ('name' in request.GET):context["name"]=request.GET['name']
	if ('publisher' in request.GET):context["publisher"]=request.GET['publisher']
	if ('language' in request.GET):context["language"]=request.GET['language']
	if ('stat' in request.GET):context["stat"]=request.GET['stat']
	if (("stat" in request.GET) and request.GET['stat']=='0'):
		if (tmp==1):whereQ+=" and "
		whereQ+=" left>0 "
		tmp=1
	
	if (tmp==1):whereQ+=" and "
	whereQ+=" number>0 "
	tmp=1	
		
	print(whereQ)
	if (tmp!=0): query+=" where "+whereQ
	query+=" order by avgscore desc,borrownum "
	print(query)
	books_list=()
	try:
		cursor.execute(query)
		books_list=cursor.fetchall()
	except Exception:
		pass
	if (len(books_list)%opbk==0): pagenum=int(len(books_list)/opbk)
	else: pagenum=int(len(books_list)/opbk+1)
	#print(pagenum)
	context['pagepre']=False if (nowpage<=1) else True
	context['pagenext']=False if (nowpage>=pagenum) else True
	context['pagepn']=nowpage-1
	context['pagenn']=nowpage+1
	pages=[]
	for i in range(1,pagenum+1):
		if (i==nowpage):pages.append(i)
		else:pages.append(i)
	print(pages)
	context['pages']=pages
	Booklist=[]

	for i in range((nowpage-1)*opbk,nowpage*opbk): 
		print(i)
		try:
			Booklist.append(books_list[i])
		except Exception:
			pass
	print(Booklist)
	context["books"]=Booklist
	res=render(request,'search.html',context)
	return res
