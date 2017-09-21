
from ..models import *
from django import template

register=template.Library()

@register.simple_tag
def get_recent_posts(num=8):
    return Post.objects.all().order_by("-create_time")[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month','DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()