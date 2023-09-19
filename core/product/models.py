from django.db import models
from colorfield.fields import ColorField
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
    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
        ("#0000ff", "blue", ),
        ("#ffd800", "yellow", ),
        ("#ff0000", "red", ),
    ]
    name = models.CharField(max_length=450,verbose_name='نام محصول')
    image = models.ImageField(verbose_name="عکس محصول")
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    brand = models.ForeignKey("home.Brand",on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    color = ColorField(samples=COLOR_PALETTE,null=True)
    discount = models.IntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)],verbose_name='درصد تخفیف')
    sales_number = models.IntegerField(default=0)
    specification = models.TextField()
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)
    is_special = models.BooleanField(default=False)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def main_discount_call(self):
        return self.price - (self.price * (self.discount/100))
    
    def calculate_price(self,count):
        return self.main_discount_call() * count
    
    def in_stock(self):
        return bool(self.count)


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
            

class WishList(models.Model):
    profile = models.OneToOneField("account.Profile",on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return str(self.id) + " " +  self.profile.get_fullname()
         
