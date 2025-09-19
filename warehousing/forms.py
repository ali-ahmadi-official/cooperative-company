from django import forms
from .models import CommodityCategory, RawMaterial, RawMaterialFactor

class RawMaterialForm(forms.ModelForm):
    filter_category = forms.ModelChoiceField(
        queryset=CommodityCategory.objects.all(),
        required=False,
        label="دسته بندی کالا"
    )

    class Meta:
        model = RawMaterial
        fields = [
            'ternal', 'category', 'filter_category', 'commodity', 'amount',
            'input_unit', 'output_unit', 'output_amount', 'purchase_date',
            'arrival_date', 'price', 'supplier', 'description',
        ]
        widgets = {
            'purchase_date': forms.TextInput(attrs={'data-jdp': '', 'autocomplete': 'off'}),
            'arrival_date': forms.TextInput(attrs={'data-jdp': '', 'autocomplete': 'off'}),
        }

    class Media:
        js = ('my_admin/js/rawmaterial.js',)

class RawMaterialFactorForm(forms.ModelForm):
    class Meta:
        model = RawMaterialFactor
        fields = ['raw_material', 'change', 'description']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.user = self.request.user
        if commit:
            instance.save()
        return instance
