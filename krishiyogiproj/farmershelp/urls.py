from django.conf.urls import url
from django.contrib import admin

from .views import (farmers_home,farms_home,farms_detail,farms_add,farms_edit,farms_delete,
	fields_add,fields_home,fields_detail,fields_edit,fields_delete,farmFrontend_home)

urlpatterns = [
    url(r'^farmers/$', farmers_home),
    url(r'^farms/$', farms_home,name = 'farms'),
    url(r'^farms/create$', farms_add,name = 'create'),
    url(r'^farms/details/(?P<id>\d+)/$', farms_detail, name='detail'),
    url(r'^farms/(?P<id>\d+)/edit/$', farms_edit, name='edit'),
    url(r'^farms/(?P<id>\d+)/delete/$', farms_delete, name='delete'),
    url(r'^fields/$', fields_home,name = 'fields'),
    url(r'^fields/create$', fields_add,name = 'fieldscreate'),
    url(r'^fields/details/(?P<id>\d+)/$', fields_detail, name='fieldsdetail'),
    url(r'^fields/(?P<id>\d+)/edit/$', fields_edit, name='fieldsedit'),
    url(r'^fields/(?P<id>\d+)/delete/$', fields_delete, name='fieldsdelete'),
    # url(r'^crops/$', crops_home),
    # url(r'^seasons/$', seasons_home),
]