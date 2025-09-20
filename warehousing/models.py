from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .jalali import Gregorian

class Unit(models.Model):
    name = models.CharField(verbose_name='نام', max_length=100)

    class Meta:
        verbose_name = 'تعریف واحد'
        verbose_name_plural = 'تعریف واحد ها'

    def __str__(self):
        return self.name
    
class Supplier(models.Model):
    name = models.CharField(verbose_name='نام', max_length=200)
    address = models.CharField(verbose_name='آدرس', max_length=500)
    phone_number = models.PositiveBigIntegerField(verbose_name='شماره همراه')
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name = 'تامین کننده'
        verbose_name_plural = 'تامین کنندگان'

    def __str__(self):
        return self.name

class RawMaterialCategory(models.Model):
    TERNAL_CHOICES = (
        ('1', 'وارداتی'),
        ('2', 'داخلی'),
    )

    ternal = models.CharField(verbose_name='نوع', choices=TERNAL_CHOICES, max_length=1)
    name = models.CharField(verbose_name='نام', max_length=100)

    class Meta:
        verbose_name = 'دسته بندی ماده اولیه'
        verbose_name_plural = 'دسته بندی های ماده اولیه'
    
    def __str__(self):
        return self.name

class CommodityCategory(models.Model):
    parent = models.ForeignKey(RawMaterialCategory, on_delete=models.CASCADE, related_name='category_categories', verbose_name='والد')
    name = models.CharField(verbose_name='نام', max_length=100)

    class Meta:
        verbose_name = 'دسته بندی کالا'
        verbose_name_plural = 'دسته بندی های کالا'

    def __str__(self):
        return self.name

class Commodity(models.Model):
    category = models.ForeignKey(CommodityCategory, on_delete=models.DO_NOTHING, related_name='category_commodities', verbose_name='دسته بندی')
    name = models.CharField(verbose_name='نام', max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, related_name='unit_commodity', verbose_name='واحد')

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا ها'
    
    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    TERNAL_CHOICES = (
        ('1', 'وارداتی'),
        ('2', 'داخلی'),
    )

    ternal = models.CharField(verbose_name='نوع', choices=TERNAL_CHOICES, max_length=1)
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.DO_NOTHING, related_name='category_raw_materials', verbose_name='دسته بندی')
    commodity_category = models.ForeignKey(CommodityCategory, on_delete=models.DO_NOTHING, related_name='commodity_category_raw_materials', verbose_name='دسته بندی کالا')
    commodity = models.ForeignKey(Commodity, on_delete=models.DO_NOTHING, related_name='commodity_raw_materials', verbose_name='کالا')
    amount = models.DecimalField(verbose_name='مقدار ورودی', max_digits=12, decimal_places=3)
    input_unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, related_name='input_unit_raw_materials', verbose_name='واحد ورودی')
    output_unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, related_name='output_unit_raw_materials', verbose_name='واحد خروجی')
    output_amount = models.DecimalField(verbose_name='مقدار خروجی (قابل مصرف)', max_digits=12, decimal_places=3)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name='supplier_raw_materials', verbose_name='تامین کننده')
    purchase_date = models.CharField(verbose_name='تاریخ خرید', max_length=10)
    arrival_date = models.CharField(verbose_name='تاریخ ورود', max_length=10)
    price = models.PositiveBigIntegerField(verbose_name='قیمت خرید هر واحد (ریال)')
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name = 'ماده اولیه'
        verbose_name_plural = 'مواد اولیه'
    
    def __str__(self):
        return f'ماده اولیه با کالای {self.commodity}'

class BuyRawMaterial(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='buy_raw_materials', verbose_name='ماده اولیه')
    change = models.PositiveIntegerField(verbose_name='مقدار خرید')

    def __str__(self):
        return f'افزایش موجودی {self.raw_material}'