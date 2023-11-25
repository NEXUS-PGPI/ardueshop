from django.contrib import admin
from .models import Product, Category, Opinion

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock', 'price', 'category']

@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ['comment', 'user', 'product']

admin.site.register(Category)
