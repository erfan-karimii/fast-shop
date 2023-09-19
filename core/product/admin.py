from django.contrib import admin
from .models import Category,CategoryDepthTwo,Product,PhotoGallery,Comment,WishList
# Register your models here.

class CustomProductAdmin(admin.ModelAdmin):
    list_display = ('name','sales_number','is_show')
    list_editable = ('is_show',)

class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_special')
    list_editable = ('is_special',)

admin.site.register(Category,CustomCategoryAdmin)
admin.site.register(CategoryDepthTwo)
admin.site.register(Product,CustomProductAdmin)
admin.site.register(PhotoGallery)
admin.site.register(Comment)
admin.site.register(WishList)


