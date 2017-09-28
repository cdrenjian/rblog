# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','create_time','modified_time','category','author']


admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)


