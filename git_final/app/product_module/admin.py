from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, ProductReview
from . import models
from .models import (
    ProductCategory,
    Product,
    ProductGallery,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

admin.site.register(ProductCategory, MPTTModelAdmin)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductGalleryInline,
    ]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_date', 'parent']


admin.site.register(models.ProductReview, ProductReviewAdmin)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
