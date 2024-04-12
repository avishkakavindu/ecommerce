from django.contrib import admin

# Register your models here.
from .models import *

class ImagesTabularinline(admin.TabularInline):
    model = Images
class TagTabularinline(admin.TabularInline):
    model = Tag
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTabularinline,TagTabularinline]
class OrderItemTabularinline(admin.TabularInline):
    model = OrderItem
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularinline]

admin.site.register(Images)
admin.site.register(Tag)

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact_us)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)