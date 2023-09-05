from django.contrib import admin
from .models import Category,CategoryDepthTwo,Product,PhotoGallery,Comment,WishList
# Register your models here.

admin.site.register(Category)
admin.site.register(CategoryDepthTwo)
admin.site.register(Product)
admin.site.register(PhotoGallery)
admin.site.register(Comment)
admin.site.register(WishList)


