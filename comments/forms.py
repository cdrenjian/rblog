#coding:utf-8

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:#内部类
        model=Comment
        fields=["name","text","url","email"]  #指明需要显示的字段