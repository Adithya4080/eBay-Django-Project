from django.contrib import admin

from web.models import Product, Category, Gallery,SavedItem,Specification


class GalleryAdmin(admin.TabularInline):
    list_display = ["name","image"]
    model = Gallery


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","price","image")
    prepopulated_fields = {"slug": ("name",)}

    inlines = [GalleryAdmin,SpecificationInline]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SavedItem)