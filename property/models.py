from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Property(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=8,decimal_places=2)
    is_active = models.BooleanField(default=True) #admin can deactive listings.
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="property_images/",blank=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "property"
        verbose_name_plural = "Properties"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings")
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8,decimal_places=2)
    approved = models.BooleanField(default=False) #admin approves booking
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.property.title}"

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reviews")
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True,null=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"

