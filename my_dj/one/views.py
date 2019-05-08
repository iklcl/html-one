# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
 
 
def home(request):
    List = map(str, range(100))# 一个长度为100的 List
    return render(request, 'home.html', {'List': List})
# Create your views here.
