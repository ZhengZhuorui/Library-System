# -*- coding: utf-8 -*-  

from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.db import connection
from Library import base
from LibData.models import Member
def FAQ(request):
	context={}
	base.init(request,context)
	res=render(request,'FAQ.html',context)
	return res
	