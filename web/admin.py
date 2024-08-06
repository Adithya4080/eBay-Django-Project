from django.contrib import admin
from web.models import Product, Category, Gallery


class GalleryAdmin(admin.TabularInline):
    list_display = ["name","image"]
    model = Gallery

admin.site.register(Product)
admin.site.register(Category)
