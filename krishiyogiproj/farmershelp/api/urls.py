from django.conf.urls import url
from django.contrib import admin

from .views import (FarmsListAPIView,
    FarmersListAPIView,
    FarmsDetailAPIView,
    FarmsDeleteAPIView,
    FarmsEditAPIView,
    FarmsAddAPIView,
    FieldsListAPIView,
    FieldsDetailAPIView,
    FieldsDeleteAPIView,
    FieldsAddAPIView,
    FieldsEditAPIView)

# farms_detail,farms_add,farms_edit,farms_delete,
# 	fields_add,fields_home,fields_detail,fields_edit,fields_delete)

urlpatterns = [
    url(r'^$', FarmersListAPIView.as_view()),
    url(r'^farms/$', FarmsListAPIView.as_view(),name = 'farms'),
    url(r'^farms/details/(?P<id>\d+)/$', FarmsDetailAPIView.as_view(), name='detail'),
    url(r'^farms/create$', FarmsAddAPIView.as_view(),name = 'create'),
    url(r'^farms/(?P<id>\d+)/edit/$', FarmsEditAPIView.as_view(), name='edit'),
    url(r'^farms/(?P<id>\d+)/delete/$', FarmsDeleteAPIView.as_view(), name='delete'),
    url(r'^fields/$', FieldsListAPIView.as_view(),name = 'fields'),
    url(r'^fields/create$', FieldsAddAPIView.as_view(),name = 'fieldscreate'),
    url(r'^fields/details/(?P<id>\d+)/$', FieldsDetailAPIView.as_view(), name='fieldsdetail'),
    url(r'^fields/(?P<id>\d+)/edit/$', FieldsEditAPIView.as_view(), name='fieldsedit'),
    url(r'^fields/(?P<id>\d+)/delete/$', FieldsDeleteAPIView.as_view(), name='fieldsdelete'),
    
    
]