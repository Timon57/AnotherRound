from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager,self).get_queryset().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("category_list", args=[self.id])
    
    
    

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    alcohol = models.IntegerField()
    volume = models.IntegerField()
    brand = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    images = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=4,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created  = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('product_detail',args=[self.id])
    

    



