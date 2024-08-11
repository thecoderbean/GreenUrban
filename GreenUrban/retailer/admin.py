from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Product, ProductImage,Retailer,Order

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"

    image_tag.short_description = 'Image'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'rating', 'available', 'created', 'updated')
    list_filter = ('available', 'created', 'updated', 'category')
    search_fields = ('name', 'description', 'category__name')
    inlines = [ProductImageInline]


@admin.register(Retailer)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'phone_number', 'address', 'registration_date')


admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
