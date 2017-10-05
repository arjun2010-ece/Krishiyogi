from django import forms

from .models import (Farms,Fields)


class FarmsForm(forms.ModelForm):
    class Meta:
        model = Farms
        fields = [
         "farm_name",
         "farm_description",
         "farmers_id_fk"
        ]

class FieldsForm(forms.ModelForm):
    class Meta:
        model = Fields
        fields = [
         "field_name",
         "field_description",
         "farm_id_fk",
         "crop_id_fk"
        ]
    