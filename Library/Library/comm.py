# -*- coding: utf-8 -*-  

from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Book
from LibData.models import comment
def comm(request,isbn,cmpg=1):
	context={}
	base.init(request,context)
	next="/book/"+isbn+"/"+cmpg+"/#L1"
	if (request.method=='POST'):
		try:
			p=Member.objects.get(name=context['Username'])
		except Exception as e:
			print(e)
			ret=redirect(next)
			print("W1")
			return ret
		try:
			b=Book.objects.get(isbn=isbn)
		except Exception as e:
			print(e)
			ret=redirect(next)
			print("W2")
			return ret
		try:
			print("O1")
			com=comment.objects.get(user=p,bookisbn=b)
			if (com.score!=-1):
				
				b.totmnt-=1
				b.totscore-=int(com.score)
				if (b.totmnt==0):b.avgscore=0
				else:b.avgscore=b.totscore/b.totmnt
				b.save()
			com.com=request.POST['comment']
			try:
				com.score=int(request.POST['score'])
			except Exception:
				com.score=-1
			com.save()
			if (com.score!=-1):
				print("totmnt:%d"%b.totmnt)
				b.totmnt+=1
				print("totmnt:%d"%b.totmnt)
				b.totscore+=int(com.score)
				b.avgscore=b.totscore/b.totmnt
				b.save()
			ret=redirect(next)
			return ret
		except Exception as e:
			print(e)
			try:
				score=int(request.POST['score'])
			except Exception:
				score=-1
			print('score:%d'%score)
			com=comment(user=p,bookisbn=b,com=request.POST['comment'],score=score)
			com.save()
			if (com.score!=-1):
				b.totmnt+=1
				b.totscore+=int(com.score)
				b.avgscore=b.totscore/b.totmnt
				b.save()
			print("OK")
			ret=redirect(next)
			return ret
