from django.conf.urls import url,include
from . import views

app_name="comments"
urlpatterns = [
    url(r'^(?P<post_pk>[0-9]+)/$',views.do_comment,name='do_comment'),

]
