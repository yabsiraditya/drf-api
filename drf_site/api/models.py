import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product/', blank=True, null=True)

    @property
    def in_stock(self):
        return self.stock > 0
    
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMATION = "Confirmation"
        CANCELLED = "Cancelled"


    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    items_order = models.ManyToManyField(
        Product, through='Purchase', related_name='Purchases'
    )


    def __str__(self):
        return f'Order {self.order_id} oleh {self.user.username}'
    

class Purchase(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    @property
    def total_price(self):
        return self.products.price * self.quantity
    

    def __str__(self):
        return f'{self.quantity} x {self.products.name} order by {self.orders.order_id}'