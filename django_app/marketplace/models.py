from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPES = (
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, max_length=500)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='freelancer')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    total_reviews = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.user_type}"
    
    class Meta:
        ordering = ['-created_at']

class Service(models.Model):
    CATEGORY_CHOICES = (
        ('web_dev', 'Web Development'),
        ('graphic_design', 'Graphic Design'),
        ('content_writing', 'Content Writing'),
        ('data_analysis', 'Data Analysis'),
        ('marketing', 'Marketing'),
        ('video_editing', 'Video Editing'),
        ('music_production', 'Music Production'),
        ('consulting', 'Consulting'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    )
    
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='services', limit_choices_to={'user_type': 'freelancer'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    service_image = models.ImageField(upload_to='services/', blank=True, null=True)
    delivery_time = models.IntegerField(default=7, help_text="Delivery time in days")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_bookings = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - ${self.price}"
    
    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings_made', limit_choices_to={'user_type': 'client'})
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings_received', limit_choices_to={'user_type': 'freelancer'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.service.title}"
    
    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review of {self.booking.service.title} - {self.rating}★"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('booking', 'reviewer')
