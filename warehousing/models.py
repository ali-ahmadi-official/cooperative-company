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

class CommodityCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category_categories', verbose_name='والد', null=True, blank=True)
    name = models.CharField(verbose_name='نام', max_length=100)

    class Meta:
        verbose_name = 'دسته بندی کالا'
        verbose_name_plural = 'دسته بندی های کالا'

    def __str__(self):
        return self.name

class Commodity(models.Model):
    TERNAL_CHOICES = (
        ('1', 'وارداتی'),
        ('2', 'داخلی'),
    )

    ternal = models.CharField(verbose_name='نوع', choices=TERNAL_CHOICES, max_length=1)
    category = models.ForeignKey(CommodityCategory, on_delete=models.DO_NOTHING, related_name='category_commodities', verbose_name='دسته بندی')
    name = models.CharField(verbose_name='نام', max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, related_name='unit_commodity', verbose_name='واحد')

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا ها'
    
    def __str__(self):
        return self.name

class RawMaterialCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category_categories', verbose_name='والد', null=True, blank=True)
    name = models.CharField(verbose_name='نام', max_length=100)

    class Meta:
        verbose_name = 'دسته بندی ماده اولیه'
        verbose_name_plural = 'دسته بندی های ماده اولیه'
    
    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    TERNAL_CHOICES = (
        ('1', 'وارداتی'),
        ('2', 'داخلی'),
    )

    ternal = models.CharField(verbose_name='نوع', choices=TERNAL_CHOICES, max_length=1)
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.DO_NOTHING, related_name='category_raw_materials', verbose_name='دسته بندی')
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

class RawMaterialFactor(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_raw_material_factors', verbose_name='کاربر')
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='raw_material_factors', verbose_name='ماده اولیه')
    change = models.IntegerField(verbose_name='مقدار تغییر')
    date = models.CharField(verbose_name='تاریخ', max_length=10)
    description = models.TextField(verbose_name='توضیحات (اختیاری)', null=True, blank=True)

    class Meta:
        verbose_name = 'فاکتور سایت'
        verbose_name_plural = 'فاکتور های سایت'
    
    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        group_names = ", ".join([group.name for group in self.user.groups.all()])
        return f"از طرف {full_name} ({group_names})"

    def save(self, *args, **kwargs):
        raw_material = self.raw_material
        ratio = raw_material.amount / raw_material.output_amount
        new_amount = raw_material.amount + self.change
        new_output_amount = raw_material.output_amount + (self.change / ratio)

        if new_amount < 0 or new_output_amount < 0:
            raise ValidationError("مقدار ماده اولیه نمی‌تواند منفی باشد.")

        if self.pk is None:
            raw_material.amount = new_amount
            raw_material.output_amount = new_output_amount
            raw_material.save()

        if not self.date:
            today = timezone.now().date()
            year, month, day = Gregorian(today.year, today.month, today.day).persian_tuple()
            persian_date = f"{year}/{month:02d}/{day:02d}"
            self.date = persian_date

        super().save(*args, **kwargs)
