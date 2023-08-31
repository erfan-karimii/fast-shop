from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام دسته بندی')
    brand = models.ManyToManyField("home.Brand")
    return_condition = models.TextField(default='برای کالاهای گروه موبایل، امکان برگشت کالا به دلیل انصراف از خرید تنها در صورتی مورد قبول است که کالا بدون هیچگونه استفاده و با تمامی قطعات، متعلقات و بسته‌بندی‌های اولیه خود بازگردانده شود. لازم به ذکر است که برای هر کالای موبایل، ضمانت رجیستری صادر می‌شود. در صورت بروز اشکال در ضمانت رجیستری، پس از انقضای مدت ۳۰ روزه، کالا می‌تواند بازگردانده شود.')
    image = models.ImageField(verbose_name='عکس دسته بندی')
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')
    is_special = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class CategoryDepthTwo(models.Model):
    parent = models.ForeignKey(Category,on_delete=models.PROTECT)
    name = models.CharField(max_length=100,verbose_name='نام زیر دسته بندی')
    link = models.CharField(max_length=100,verbose_name='لینک زیر دسته بندی')    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=450,verbose_name='نام محصول')
    image = models.ImageField(verbose_name="عکس محصول")
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    brand = models.ForeignKey("home.Brand",on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    discount = models.IntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)],verbose_name='درصد تخفیف')
    specification = models.TextField()
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)
    is_show = models.BooleanField(default=True)


    def main_discount_call(self):
        return self.price - (self.price * (self.discount/100))
    
    def __str__(self):
        return self.name


class PhotoGallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    image = models.ImageField(verbose_name="عکس محصول")
    text = models.CharField(max_length=150)


class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    author = models.ForeignKey("account.Profile",on_delete=models.CASCADE)
    title = models.CharField(max_length=150) 
    text = models.TextField()
    score = models.PositiveSmallIntegerField(verbose_name='امتیاز محصول',validators=[MaxValueValidator(10)],null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=False,verbose_name='نمایش داده شود؟')
    def __str__(self):
        return self.title
            

    
