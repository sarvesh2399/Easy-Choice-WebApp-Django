from django.contrib import admin
from easychoiceapp.models import product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'cat', 'is_active']
    list_filter = ['cat', 'is_active']



admin.site.register(product, ProductAdmin)    #To create table in admin website to add products

