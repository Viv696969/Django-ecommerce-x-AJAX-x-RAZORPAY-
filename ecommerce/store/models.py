from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):

    name=models.CharField(max_length=150,null=False,blank=False,unique=True)
    category_image=models.ImageField(upload_to='images/categories',null=True,blank=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    description=models.TextField()
    product_image=models.ImageField(upload_to='images/products', default='images/products/default.png')
    quantity=models.PositiveIntegerField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False)
    trending=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(blank=False,null=False)
    created_at=models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Order(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    f_name=models.CharField(max_length=150,null=False,blank=False)
    l_name=models.CharField(max_length=150,null=False,blank=False)
    email=models.EmailField(max_length=150,null=False,blank=False)
    address=models.TextField(max_length=150,null=False,blank=False)
    phone=models.CharField(max_length=150,null=False,blank=False)
    city=models.CharField(max_length=150,null=False,blank=False)
    state=models.CharField(max_length=150,null=False,blank=False)
    pin=models.CharField(max_length=150,null=False,blank=False)
    total_price=models.FloatField(null=False,blank=False)
    payment_mode=models.CharField(max_length=150,null=False,blank=False)
    payment_id=models.CharField(max_length=150,null=True,blank=True)

    orderstatuses=(
        ('pending','pending'),
        ('out for shipping','out for shipping'),
        ('completed','completed')
    )

    status=models.CharField(choices=orderstatuses,max_length=150,default='pending')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=150,null=True)
    placed_at=models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)

    def __str__(self):
        return '{}--{}'.format(self.order.id,self.order.tracking_no)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=150,null=False,blank=False)
    last_name=models.CharField(max_length=150,null=False,blank=False)
    email=models.EmailField(max_length=150,null=False,blank=False)
    address=models.TextField(max_length=150,null=False,blank=False)
    phone=models.CharField(max_length=150,null=False,blank=False)
    city=models.CharField(max_length=150,null=False,blank=False)
    state=models.CharField(max_length=150,null=False,blank=False)
    pin=models.CharField(max_length=150,null=False,blank=False)
    

