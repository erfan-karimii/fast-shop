from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام دسته بندی')
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
    