from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect

from .models import (Farmers,Farms,Fields)

from .forms import (FarmsForm,FieldsForm)

# Create your views here.


def farms_add(request):
	form = FarmsForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
       "form":form,
	}
	return render(request,"form.html", context)


def farmers_home(request):
	queryset = Farmers.objects.all()
	context={
	 "objectlist":queryset
	}
	return render(request,"farmers.html", context)
	
def farms_home(request):
	queryset = Farms.objects.all()
	context = {
	"objectlist":queryset
	}
	return render(request,"farms_home.html", context)


def farms_detail(request,id=None):
	instance = get_object_or_404(Farms,id=id)
	context = {
	"object":instance
	}
	return render(request,"farm_detail.html", context)


def farms_edit(request,id=None):
	instance = get_object_or_404(Farms,id=id)
	form = FarmsForm(request.POST or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
	"object":instance,
	"form":form,
	}
	return render(request,"form.html", context)

def farms_delete(request,id=None):
	instance = get_object_or_404(Farms,id=id)
	instance.delete()
	return redirect("farmershelp:farms")


def fields_add(request):
	form = FieldsForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
       "form":form,
	}
	return render(request,"form.html", context)

	
def fields_home(request):
	queryset = Fields.objects.all()
	context = {
	"objectlist":queryset
	}
	return render(request,"fields_home.html", context)


def fields_detail(request,id=None):
	instance = get_object_or_404(Fields,id=id)
	context = {
	"object":instance
	}
	return render(request,"field_detail.html", context)


def fields_edit(request,id=None):
	instance = get_object_or_404(Fields,id=id)
	form = FarmsForm(request.POST or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
	"object":instance,
	"form":form,
	}
	return render(request,"form.html", context)

def fields_delete(request,id=None):
	instance = get_object_or_404(Farms,id=id)
	instance.delete()
	return redirect("farmershelp:fields")


