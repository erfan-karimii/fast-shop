from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
# Create your models here.



def validate_phone_number(value):
    if  not bool(re.compile("^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$").match(value)):
        raise ValidationError(
            _('number is not valid'),
        )

class Order(models.Model):
    profile = models.ForeignKey('account.Profile',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250,null=True,blank=True)
    last_name = models.CharField(max_length=250,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    phone_number = models.CharField(max_length=15,validators=[validate_phone_number],null=True,blank=True)
    zip_code = models.CharField(max_length=30,null=True)
    national_code = models.CharField(max_length=10,null=True)
    paid_amount = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    stripe_token = models.CharField(max_length=100,null=True,blank=True)
    payment_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return str(self.profile) + " ////////// " + str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order.id) + " ////////// " + self.product.name