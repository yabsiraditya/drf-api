import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import User, Product, Order, Purchase


class Command(BaseCommand):
    help = 'Membuat data dummy aplikasi'

    def handle(self, *args, **kwargs):
        # dapatkan atau buat superuser
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(
                username='admin', password='test')

        # buat produk - name, description, price, stok, gambar
        products = [
            Product(name="Macbook Pro 16", description=lorem_ipsum.paragraph(), 
                price=Decimal('9999.9'), stock=4),
            Product(name="Mesin Kopi", description=lorem_ipsum.paragraph(), 
                price=Decimal('200.1'), stock=6),
            Product(name="Speaker Simbada", description=lorem_ipsum.paragraph(),
                price=Decimal('15.99'), stock=11),
            Product(name="Iphone 16 Pro Max", description=lorem_ipsum.paragraph(), 
                price=Decimal('1250.0'), stock=2),
            Product(name="Kamera Digital", description=lorem_ipsum.paragraph(),
                price=Decimal('350.99'), stock=4),
            Product(name="Apple Watch", description=lorem_ipsum.paragraph(),
                price=Decimal('500.05'), stock=0),
        ]

        # buat Product & ambil ulang dari DB
        Product.objects.bulk_create(products)
        products = Product.objects.all()

        # buat beberapa perintah tiruan yang terikat pada superuser
        for _ in range(3):
            # buat Pesanan dengan 2 item pesanan
            order = Order.objects.create(user=user)
            for product in random.sample(list(products), 2):
                Purchase.objects.create(
                    orders=order, products=product, quantity=random.randint(1, 3)
                )