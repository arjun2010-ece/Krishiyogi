from django.contrib import admin

# Register your models here.

from .models import (Farmers,Farms,Seasons,Crops,Fields)


admin.site.register(Farmers)
admin.site.register(Seasons)
admin.site.register(Farms)
admin.site.register(Crops)
admin.site.register(Fields)