from django.contrib import admin
from .models import UserProfile, Service, Booking, Review

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'rating', 'is_verified', 'created_at']
    list_filter = ['user_type', 'is_verified', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['rating', 'total_reviews', 'created_at', 'updated_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'category', 'price', 'status', 'rating', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'description', 'freelancer__user__username']
    readonly_fields = ['rating', 'total_bookings', 'created_at', 'updated_at']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'client', 'freelancer', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['service__title', 'client__user__username', 'freelancer__user__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['booking__service__title', 'reviewer__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
