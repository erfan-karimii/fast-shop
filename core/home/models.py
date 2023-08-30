from django.db import models

# Create your models here.

class TemplateSettings(models.Model):
    top_navbar = models.ImageField()
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')
    logo = models.ImageField(verbose_name='بنر میانی راست')
    banner1 = models.ImageField()
    alt1 = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')
    banner2 = models.ImageField(verbose_name='بنر میانی چپ')
    alt2 = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')
    banner3 = models.ImageField(verbose_name='بنر میانی پایین')
    alt3 = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')


class UnderSlider(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام')
    image = models.ImageField(verbose_name='عکس زیر اسلایدر')
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')

    def __str__(self):
        return self.name
 

class Brands(models.Model):
    image = models.ImageField(verbose_name='عکس برند')
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')


class NavBar(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام نوبار')
    link = models.CharField(max_length=100,verbose_name='لینک نوبار')
    icon = models.CharField(max_length=50,verbose_name='ایکون')    
    def __str__(self):
        return self.name


class NavBarDepthTwo(models.Model):
    parent = models.ForeignKey(NavBar,on_delete=models.PROTECT)
    name = models.CharField(max_length=100,verbose_name='نام نوبار')
    link = models.CharField(max_length=100,verbose_name='لینک نوبار')    
    def __str__(self):
        return self.name


class Slider(models.Model):
    image = models.ImageField(verbose_name='عکس سلایدر')
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True,blank=True,default='image')
    link = models.CharField(max_length=100,verbose_name='ادرس دکمه')
    def __str__(self):
        return self.image + " | " + self.link
    

class Footer(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class FooterDepthTwo(models.Model):
    parent = models.ForeignKey(Footer,on_delete=models.PROTECT)
    name = models.CharField(max_length=50,verbose_name='نام')
    link = models.CharField(max_length=100,null=True,verbose_name='لینک صفحه')
    def __str__(self):
        return  str(self.parent.name) + " | " +  self.name 
