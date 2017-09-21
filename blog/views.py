# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from models import *
import markdown
from comments.forms import CommentForm

# Create your views here.
def index(request):
    post_list=Post.objects.all()
    return render(request,"blog/index.html",locals())
def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.increase()
    post.body=markdown.markdown(post.body,extensions=["markdown.extensions.extra","markdown.extensions.codehilite","markdown.extensions.toc",])
    form=CommentForm()  #生成表单实例
    comment_list=post.comment_set.all()
    return render(request,'blog/detail.html',locals())
def archives(request,year,month):
    post_list=Post.objects.filter(create_time__year=year,create_time__month=month)
    return render(request,"blog/index.html",locals())
def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate)
    return render(request,'blog/index.html',locals())