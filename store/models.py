from django.db import models
from django.contrib.auth.models import User


# ================= PRODUCT =================
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


# ================= ORDER =================
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=20, default='PLACED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.product_name


# ================= LIFE EVENTS =================
class LifeEvent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EventProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    event = models.ForeignKey(LifeEvent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.event.name}"


# ================= GROUP BUYING =================
class GroupDeal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    group_price = models.IntegerField()
    min_users = models.IntegerField(default=3)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Group Deal - {self.product.name}"


class GroupDealMember(models.Model):
    group_deal = models.ForeignKey(GroupDeal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} joined {self.group_deal.product.name}"


# ================= REVIEWS & RATINGS =================
class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}⭐ by {self.user.username}"


# ================= WISHLIST ❤️ =================
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.name}"
