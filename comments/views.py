# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404,redirect
from .forms import CommentForm
from .models import Comment
from blog.models import Post

def do_comment(request,post_pk):
    post=get_object_or_404(Post,pk=post_pk)
    if request.method=="POST":
        form=CommentForm(request.POST)    #构造表单实例
        if form.is_valid():
            comment=form.save(commit=False)  #生成数据库模型实例，但是不保存数据到数据库
            comment.post=post
            comment.save()#提交数据到数据库
            return redirect(post)
        else:
            comment_list=post.comment_set.all()
            context={
                "form":form,
                "post":post,
                "comment_list":comment_list
            }
            return  render(request,"blog/detail.html",context=context)
    else:
        return redirect(post)


