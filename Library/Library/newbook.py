# -*- coding: utf-8 -*-  
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
from LibData.models import Book
import os
@csrf_exempt
def newbook(request):
	context={}
	base.init(request,context)
	context["Err"]=0
	context['Succ']=0
	if (context['HaveLogin']!=1):
		context['Err']=1
		context['ErrMsg']="请先登录"
		ret=render(request,'newbook.html',context)
		return ret
	if (request.method=='GET'):
		if ('isbn' in request.GET): 
			context['isbn']=request.GET['isbn']
			try:
				p=Book.objects.get(isbn=context['isbn'])
				context['name']=p.name
				context['publisher']=p.publisher
				context['number']=p.number
				context['author']=p.author
				context['language']=p.language
				context['price']=p.price
				context['description']=p.description
			except Exception as e:
				print(e)
				pass
		ret=render(request,'newbook.html',context)
		return ret
	else:
		context['isbn']=request.POST['isbn']
		try:
			p=Book.objects.get(isbn=context['isbn'])
			context['name']=p.name
			context['publisher']=p.publisher
			context['number']=p.number
			context['author']=p.author
			context['language']=p.language
			context['price']=p.price
			context['description']=p.description
		except Exception:
				pass	
		if (1):
			isbn=request.POST['isbn']
			author=request.POST['author']
			print('author:%s'%author)
			name=request.POST['bookname']
			publisher=request.POST['publisher']
			number=int(request.POST['number'])
			left=number
			language=int(request.POST['language'])
			price=float(request.POST['price'])
			description=request.POST['description']
			try:
				p=Book.objects.get(isbn=isbn)
				if (number-(p.number-p.left)<0):
					context['Err']=1
					context['ErrMsg']="剩余的书少于书的减少量，无法操作"
					ret=render(request,'newbook.html',context)
					return ret
				p.name=name
				p.author=author
				p.publisher=publisher
				p.number=number
				p.left=left+(number-p.number)
				p.language=language
				p.price=price
				p.description=description
				p.save()
				print("Succ?")
				if ('image' in request.FILES):
					image=request.FILES['image']
					root=r"home/Library/static/img/book_"+p.isbn+".jpg"
					print(root)
					#print(image,type(image))
					fl=open(root,'wb')
					print("OPENSUCC")
					for chunk in image.chunks():
						fl.write(chunk)
					fl.close()
				context['Succ']=1
				ret=render(request,"newbook.html",context)
				return ret
			except Exception:
			
				p=Book(isbn,name,publisher,number,left,language,price,description,totmnt=0,totscore=0,avgscore=0,author=author)
				p.save()
				if ('image' in request.FILES):
					image=request.FILES['image']
					root=r"home/Library/static/img/book_"+p.isbn+".jpg"
					print(root)
					#print(image,type(image))
					fl=open(root,'wb')
					print("OPENSUCC")
					for chunk in image.chunks():
						fl.write(chunk)
					fl.close()
				context['Succ']=1
				ret=render(request,"newbook.html",context)
				return ret
				context['Succ']=1

				ret=render(request,"newbook.html",context)
				return ret
