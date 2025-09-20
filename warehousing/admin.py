from django.contrib import admin
from django.urls import path, reverse
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django import forms
from .models import Unit, Supplier, RawMaterialCategory, RawMaterial, Commodity, CommodityCategory
from .forms import RawMaterialForm, BuyRawMaterialForm

class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone_number']
    search_fields = ['name']

class CommodityCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']

class CommodityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'unit']
    list_filter = ['category', 'unit']
    search_fields = ['name']

class RawMaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ternal']
    list_filter = ['ternal']
    search_fields = ['name']

class RawMaterialAdmin(admin.ModelAdmin):
    form = RawMaterialForm
    list_display = ['id', 'add_buy_material_icon', 'ternal', 'category', 'commodity_category', 'commodity', 'get_amount', 'input_unit', 'get_output_amount', 'output_unit']
    list_filter = ['ternal', 'category', 'commodity_category', 'input_unit', 'output_unit']

    class Media:
        js = ('my_admin/js/buy_raw_material.js',)

    def get_amount(self, obj):
        return int(obj.amount)
    get_amount.short_description = 'مقدار ورودی'

    def get_output_amount(self, obj):
        return int(obj.amount)
    get_output_amount.short_description = 'مقدار خروجی (قابل مصرف)'

    def add_buy_material_icon(self, obj):
        return format_html(
            '''
            <a href="#" class="open-submodel-modal" data-main-id="{}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="color: #5409DA;"
                    class="bi bi-arrow-up-circle-fill" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 0 0 8a8 8 0 0 0 16 0m-7.5 3.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707z"/>
                </svg>
            </a>
            ''',
            obj.id
        )
    add_buy_material_icon.allow_tags = True
    add_buy_material_icon.short_description = 'خرید'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-submodel/<int:main_id>/', self.admin_site.admin_view(self.add_submodel_view), name='add_submodel'),
        ]
        return custom_urls + urls

    def add_submodel_view(self, request, main_id):
        raw_material = RawMaterial.objects.get(pk=main_id)

        if request.method == 'POST':
            form = BuyRawMaterialForm(request.POST)
            if form.is_valid():
                sub = form.save(commit=False)
                sub.raw_material = raw_material
                change = form.cleaned_data['change']

                ratio = raw_material.amount / raw_material.output_amount if raw_material.output_amount else 1
                new_amount = raw_material.amount + change
                new_output_amount = raw_material.output_amount + (change / ratio)

                raw_material.amount = new_amount
                raw_material.output_amount = new_output_amount
                raw_material.save()

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        else:
            form = BuyRawMaterialForm()
            context = dict(
                self.admin_site.each_context(request),
                form=form,
                main=raw_material,
                action_url = reverse('admin:add_submodel', args=[main_id])
            )
            return TemplateResponse(request, "admin/add_buy_raw_material_modal.html", context)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != 'price']
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "commodity":
            if request.GET.get('commodity_category'):
                kwargs['queryset'] = Commodity.objects.filter(
                    category_id=request.GET.get('commodity_category')
                )
            else:
                kwargs['queryset'] = Commodity.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Unit, UnitAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(CommodityCategory, CommodityCategoryAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(RawMaterialCategory, RawMaterialCategoryAdmin)
admin.site.register(RawMaterial, RawMaterialAdmin)