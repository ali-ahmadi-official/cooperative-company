from django.contrib import admin
from .models import Unit, Supplier, RawMaterialCategory, RawMaterial, RawMaterialFactor, Commodity, CommodityCategory
from .forms import RawMaterialForm, RawMaterialFactorForm

class RawMaterialFactorInline(admin.StackedInline):
    model = RawMaterialFactor
    fk_name = 'raw_material'
    fields = ['change', 'date', 'description']
    extra = 0
    show_change_link = False
    readonly_fields = [field.name for field in RawMaterialFactor._meta.fields if field.name != 'id']

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj = ...):
        return False

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
    inlines = [RawMaterialFactorInline]
    list_display = ['id', 'ternal', 'category', 'commodity_category', 'commodity', 'input_unit', 'output_unit', 'amount', 'output_amount']
    list_filter = ['ternal', 'category', 'commodity_category', 'input_unit', 'output_unit']

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

class RawMaterialFactorAdmin(admin.ModelAdmin):
    form = RawMaterialFactorForm
    list_display = ['id', 'get_user_full_name', 'raw_material', 'change', 'date']
    list_filter = ['user', 'raw_material']
    search_fields = ['date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_user_full_name(self, obj):
        full_name = obj.user.get_full_name() or obj.user.username
        if obj.user.is_superuser:
            return f"{full_name} (مدیرعامل)"
        group_names = ", ".join([group.name for group in obj.user.groups.all()])
        return f"{full_name} ({group_names})"
    get_user_full_name.short_description = 'کاربر'

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)

        class FormWithRequest(form_class):
            def __init__(self2, *args, **kwargs):
                kwargs['request'] = request
                super().__init__(*args, **kwargs)

        return FormWithRequest

admin.site.register(Unit, UnitAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(CommodityCategory, CommodityCategoryAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(RawMaterialCategory, RawMaterialCategoryAdmin)
admin.site.register(RawMaterial, RawMaterialAdmin)
admin.site.register(RawMaterialFactor, RawMaterialFactorAdmin)