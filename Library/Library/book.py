# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Book
from LibData.models import comment
def commnt(context,p,cmpg,m):
	query="select *  from LibData_comment where bookisbn_id='"+p.isbn+"' order by date desc "
	opbk=5
	print(query)
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		com_list=cursor.fetchall()
	except Exception as e:
		print(e)
	if (len(com_list)%opbk==0): pagenum=int(len(com_list)/opbk)
	else: pagenum=int(len(com_list)/opbk+1)
	context['pagepre']=False if (cmpg<=1) else True
	context['pagenext']=False if (cmpg>=pagenum) else True
	context['pagep']=cmpg-1
	context['pagen']=cmpg+1
	context['comnum']=len(com_list)
	cmmlist=[]
	for i in range((cmpg-1)*opbk,cmpg*opbk): 
		try:
			cmmlist.append(com_list[i])
		except Exception:
			pass
	print(cmmlist)
	context['comms']=cmmlist
	context['cmpg']=cmpg
	context['comed']=0
	context['commnt']=""
	try:
		mnt=comment.objects.get(user=m,bookisbn=p)
		context['comed']=1
		context['commnt']=mnt.com
	except Exception as e:
		print(e)
		pass
		
def book(request,isbp,cmpg=1):
	context={}
	base.init(request,context)
	a=isbp
	try:
		p=Book.objects.get(isbn=a)
		print("B1")
	except Exception:
		pass
		
	m=0
	try:
		m=Member.objects.get(name=context['Username'])
		print("M1")
		context['level']=m.level
	except Exception:
		context['level']=-1
	
	context['name']=p.name
	context['isbn']=p.isbn
	context['publisher']=p.publisher
	if (p.language==1): context['language']="汉语"
	if (p.language==2): context['language']="英语"
	if (p.language==3): context['language']="其他"
	context['description']=p.description
	context['number']=p.number
	context['left']=p.left
	context['price']=p.price
	context['avgscore']=p.avgscore
	context['author']=p.author
	commnt(context,p,cmpg,m)
	print(context)
	ret=render(request,'book.html',context)
	return ret
