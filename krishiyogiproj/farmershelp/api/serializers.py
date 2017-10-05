from rest_framework.serializers import ModelSerializer

from farmershelp.models import (Farms,Farmers,Fields)



class FarmSerializers(ModelSerializer):
	class Meta:
		model = Farms
		fields = ['farm_name','farm_description','farmers_id_fk',]

class FarmDetailsSerializers(ModelSerializer):
	class Meta:
		model = Farms
		fields = ['id','farm_name','farm_description','farmers_id_fk',]


class FarmCreateSerializers(ModelSerializer):
	class Meta:
		model = Farms
		fields = ['farm_name','farm_description','farmers_id_fk',]

class FieldSerializers(ModelSerializer):
	class Meta:
		model = Fields
		fields = ['field_name','field_description','farm_id_fk','crop_id_fk']

class FieldDetailsSerializers(ModelSerializer):
	class Meta:
		model = Fields
		fields = ['id','field_name','field_description','farm_id_fk','crop_id_fk']


class FieldCreateSerializers(ModelSerializer):
	class Meta:
		model = Fields
		fields = ['field_name','field_description','farm_id_fk','crop_id_fk']


class FarmerSerializers(ModelSerializer):
	class Meta:
		model = Farmers
		fields=['FarmerName','FarmingExperience','No_of_family','updated','timestamp']