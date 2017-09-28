# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from models import *
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView,DayArchiveView


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context=super(IndexView, self).get_context_data(**kwargs)
        paginator=context.get("paginator")
        page=context.get('page_obj')
        is_paginated=context.get("is_paginated")
        pagination_data=self.get_pagination_data(paginator,page,is_paginated)
        context.update({"page_range":pagination_data})
        return context
    def get_pagination_data(self,paginator,page,is_paginated):  #处理页码数据，将附近页码显示，较远省略，首尾显示。
        if not is_paginated:
            return {}
        page_num=page.number
        total_page=paginator.num_pages
        page_range=list(paginator.page_range)
        if page_num-3>0:
            page_range[1:page_num-3]=["." for i in range(1,page_num-3)]
        if page_num+3<total_page:
            page_range[page_num+2:total_page-1]=["." for i in range(page_num+2,total_page-1)]
        return page_range

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    def get(self, request, *args, **kwargs):
        response=super(PostDetailView, self).get(request,*args,**kwargs)   #调用父类get方法后，才会有object实例，其值即为单个的post
        self.object.increase()
        return response
    def get_object(self, queryset=None):   #该方法在get中被调用，用于获取对象实例
        post=super(PostDetailView, self).get_object(queryset=None)
        post.body=post.get_markdown()
        return post
    def get_context_data(self, **kwargs):   #装配需要的模板变量值
        context=super(PostDetailView, self).get_context_data(**kwargs)   #将post对象和其键名匹配起来加入字典
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        context.update({"form":form,"comment_list":comment_list})
        return context

class ArchivesView(IndexView):
    def get_queryset(self):
        year=self.kwargs.get("year")
        month=self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year,create_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super(TagView, self).get_queryset().filter(tags=tag)

