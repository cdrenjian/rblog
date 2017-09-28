# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Tag(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=70)
    body=models.TextField()
    create_time=models.DateTimeField()
    modified_time=models.DateTimeField()
    excerpt=models.CharField(max_length=200,blank=True)
    category=models.ForeignKey(Category)
    tags=models.ManyToManyField(Tag)
    author=models.ForeignKey(User)
    views=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    def increase(self):
        self.views+=1
        self.save(update_fields=["views"])
    def get_markdown(self):
        return markdown.markdown(self.body, extensions=["markdown.extensions.extra", "markdown.extensions.codehilite",
                                                 "markdown.extensions.toc", ])
    class Meta:
        ordering=["-create_time"]
    def save(self,*args,**kwargs): #重写sava方法，保存数据时会优先调用该方法。
        if not self.excerpt:
            self.excerpt=strip_tags(self.get_markdown())[:100]
        super(Post, self).save(*args,**kwargs)  #调用父类方法






