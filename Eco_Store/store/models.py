from django.db import models
from django.conf import settings  
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_pics/', default='about.jpg')

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    products = models.ManyToManyField(Product, through='CartItem')

    def get_total(self):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
