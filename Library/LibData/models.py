# -*- coding: utf-8 -*-  

from django.db import models

# Create your models here.
class Member(models.Model):
	name=models.CharField(max_length=20,unique=True,primary_key=True)
	realname=models.CharField(max_length=20,default="")
	password=models.CharField(max_length=20)
	level=models.IntegerField(default=0)
	email=models.EmailField(unique=True)
	bownum=models.IntegerField(default=0)
	readbook=models.IntegerField(default=1)
	def __unicode__(self):
		return self.name
class Book(models.Model):
	isbn=models.CharField(max_length=20,unique=True,primary_key=True)
	name=models.CharField(max_length=20)
	publisher=models.CharField(max_length=20,default="")
	#bookurl=models.CharField(max_length=100,default="")
	left=models.IntegerField(default=0)
	number=models.IntegerField(default=0)
	language=models.IntegerField(default=0)
	price=models.FloatField(default=0)
	description=models.CharField(max_length=2048,default="")
	borrownum=models.IntegerField(default=0)
	totmnt=models.IntegerField(default=0)
	totscore=models.IntegerField(default=0)
	avgscore=models.FloatField(default=0)
	author=models.CharField(max_length=100,default="")
	def __unicode__(self):
		return self.name
class Borrow(models.Model):
	user=models.ForeignKey('Member',on_delete=models.CASCADE)
	bookisbn=models.ForeignKey('Book',on_delete=models.CASCADE)
	st_date=models.DateField(auto_now_add=True)
	en_date=models.DateField(default="2100-01-01")
	status=models.IntegerField(default=0)
class comment(models.Model):
	user=models.ForeignKey('Member',on_delete=models.CASCADE)
	bookisbn=models.ForeignKey('Book',on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now_add=True)
	com=models.CharField(max_length=2018,default="")
	score=models.IntegerField(default=-1)
	class Meta:
		unique_together=('user','bookisbn')
