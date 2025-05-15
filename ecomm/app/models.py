from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# -------------------------------
# CATEGORY MODEL
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Optional category description

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# -------------------------------
# PRODUCT MODEL
# -------------------------------
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


# -------------------------------
# WISHLIST MODEL
# -------------------------------
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.product.name}"


# -------------------------------
# PURCHASE MODEL
# -------------------------------
class Purchase(models.Model):
    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
    )

    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_bought = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(blank=True, null=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    admin_notes = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} bought {self.product.name} on {self.date_bought.strftime('%Y-%m-%d %H:%M')}"

    def get_total_price(self):
        return self.product.price * self.quantity


# -------------------------------
# CART MODEL
# -------------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'session_key')  # Prevent duplicate carts

    def __str__(self):
        return f"Cart ({self.user.username if self.user else f'Session {self.session_key}'})"


# -------------------------------
# CART ITEM MODEL
# -------------------------------
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def subtotal(self):
        return self.quantity * self.product.price





class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 to 5
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # Prevent duplicate ratings

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} - {self.rating} Stars"
    
# Add this to your models.py file

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}'s address in {self.city}"
    
    def save(self, *args, **kwargs):
        # If this address is being set as default, unset all other defaults for this user
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        
        # If this is the first address for the user, make it default
        if not self.pk and not Address.objects.filter(user=self.user).exists():
            self.is_default = True
            
        super().save(*args, **kwargs)    
    
    
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    search_query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username if self.user else f'Session {self.session_key}'} - {self.search_query}"
    
    class Meta:
        verbose_name_plural = "Search Histories"
        # Order by most recent searches first
        ordering = ['-timestamp']