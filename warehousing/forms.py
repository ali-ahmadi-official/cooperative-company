from django import forms
from .models import RawMaterial, BuyRawMaterial

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = [
            'ternal', 'category', 'commodity_category', 'commodity', 'amount',
            'input_unit', 'output_unit', 'output_amount', 'purchase_date',
            'arrival_date', 'price', 'supplier', 'description',
        ]
        widgets = {
            'purchase_date': forms.TextInput(attrs={'data-jdp': '', 'autocomplete': 'off'}),
            'arrival_date': forms.TextInput(attrs={'data-jdp': '', 'autocomplete': 'off'}),
        }

    class Media:
        js = ('my_admin/js/rawmaterial.js',)

class BuyRawMaterialForm(forms.ModelForm):
    class Meta:
        model = BuyRawMaterial
        fields = ['change']