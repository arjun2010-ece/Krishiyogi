from rest_framework.generics import (ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView)

from farmershelp.models import (Farms,Farmers,Fields)

from .serializers import (FarmSerializers,
	FarmerSerializers,
	FarmDetailsSerializers,
	FarmCreateSerializers,
	FieldSerializers,
	FieldDetailsSerializers,
	FieldCreateSerializers)


class FarmersListAPIView(ListAPIView):
	queryset = Farmers.objects.all()
	serializer_class = FarmerSerializers



class FarmsListAPIView(ListAPIView):
	queryset = Farms.objects.all()
	serializer_class = FarmSerializers


class FarmsDetailAPIView(RetrieveAPIView):
	queryset = Farms.objects.all()
	serializer_class = FarmDetailsSerializers
	lookup_field = 'id'

class FarmsDeleteAPIView(DestroyAPIView):
	queryset = Farms.objects.all()
	serializer_class = FarmDetailsSerializers
	lookup_field = 'id'

class FarmsEditAPIView(UpdateAPIView):
	queryset = Farms.objects.all()
	serializer_class = FarmDetailsSerializers
	lookup_field = 'id'

class FarmsAddAPIView(CreateAPIView):
	queryset = Farms.objects.all()
	serializer_class = FarmCreateSerializers

class FieldsListAPIView(ListAPIView):
	queryset = Fields.objects.all()
	serializer_class = FieldSerializers


class FieldsDetailAPIView(RetrieveAPIView):
	queryset = Fields.objects.all()
	serializer_class = FieldDetailsSerializers
	lookup_field = 'id'

class FieldsDeleteAPIView(DestroyAPIView):
	queryset = Fields.objects.all()
	serializer_class = FieldDetailsSerializers
	lookup_field = 'id'

class FieldsEditAPIView(UpdateAPIView):
	queryset = Fields.objects.all()
	serializer_class = FieldDetailsSerializers
	lookup_field = 'id'

class FieldsAddAPIView(CreateAPIView):
	queryset = Fields.objects.all()
	serializer_class = FieldCreateSerializers