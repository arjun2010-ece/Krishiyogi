from django import forms

from .models import (Farms,Fields)


class FarmsForm(forms.ModelForm):
    class Meta:
        model = Farms
        fields = [
         "farm_name",
         "farm_description",
         "locationn",
         "farmers_id_fk"
        ]

class FieldsForm(forms.ModelForm):
    class Meta:
        model = Fields
        fields = [
         "field_name",
         "field_description",
         "locationn",
         "farm_id_fk",
         "crop_id_fk"
        ]
        