from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.gis.db import models

# Create your models here.
# MVC


class Farmers(models.Model):
	FarmerName = models.CharField(max_length = 120,unique=True)
	FarmingExperience = models.CharField(max_length = 120)
	No_of_family = models.CharField(max_length = 120)
	updated = models.DateTimeField(auto_now = True, auto_now_add= False)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

	def __str__(self):
		return self.FarmerName


class Farms(models.Model):
	farm_name = models.CharField(max_length = 120)
	farm_description = models.TextField()
	locationn = models.MultiPolygonField(null=True)
	objects = models.GeoManager()
	farmers_id_fk = models.ForeignKey(Farmers, on_delete = models.CASCADE)

	def __str__(self):
		return self.farm_name

	def get_absolute_url(self):
		return reverse("farmershelp:detail",kwargs={"id":self.id})


class Seasons(models.Model):
	season_name = models.CharField(max_length = 120)
	season_description = models.TextField()

	def __str__(self):
		return self.season_name

class Crops(models.Model):
	crop_name = models.CharField(max_length = 120)
	crop_description = models.TextField()
	seasons_id_fk = models.ForeignKey(Seasons,on_delete = models.CASCADE)

	def __str__(self):
		return self.crop_name


class Fields(models.Model):
	field_name = models.CharField(max_length = 120)
	field_description = models.TextField()
	locationn = models.PolygonField(default='POLYGON EMPTY')
	objects = models.GeoManager()
	farm_id_fk = models.ForeignKey(Farms,on_delete = models.CASCADE)
	crop_id_fk = models.ForeignKey(Crops,on_delete = models.CASCADE)
	
	def __str__(self):
		return self.field_name

	def get_absolute_url(self):
		return reverse("farmershelp:fieldsdetail",kwargs={"id":self.id})
		