from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )
    image = models.ImageField(upload_to='img/')


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name='sub_category',
        null=True
    )
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )
    image = models.ImageField(upload_to='img/')


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name='products',
        null=True
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete = models.CASCADE,
        related_name='products',
        null=True
    )
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )
    large_image = models.ImageField(upload_to='img/')
    medium_image = models.ImageField(upload_to='img/')
    small_image = models.ImageField(upload_to='img/')
    price = models.PositiveIntegerField()


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    @receiver(post_save, sender=User)
    def cart_create(sender, instance, created=False,  **kwargs):
        if created:
            Cart.objects.create(user=instance)


class ProductCart(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='product_cart'

    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_cart'
    )
    amount = models.PositiveIntegerField(
        default=0
    )
