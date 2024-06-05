from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class product(models.Model):
    name=models.CharField(max_length=40, verbose_name = "Product name")
    price=models.FloatField()
    # pdetails=models.CharField(max_length=150, verbose_name = "Product details")
    CAT =((1, 'Pens'),(2, 'Calculators'),(3, 'Art & Colors'),(4, 'Diaries & Notebooks'))
    cat=models.IntegerField(verbose_name = "Category", choices = CAT)
    is_active=models.BooleanField(default=True, verbose_name = "Available")
    pimage = models.ImageField(upload_to='image')

    
class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = "uid")
    pid = models.ForeignKey(product, on_delete = models.CASCADE, db_column = "pid")
    qty = models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = "uid")
    pid = models.ForeignKey(product, on_delete = models.CASCADE, db_column = "pid")
    qty = models.IntegerField(default=1)
