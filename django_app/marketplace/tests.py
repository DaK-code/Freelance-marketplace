# marketplace/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile, Service, Booking

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        
    def test_profile_creation(self):
        profile = self.user.profile
        self.assertEqual(profile.user_type, 'freelancer')
        self.assertEqual(profile.user, self.user)

class ServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='freelancer1', password='pass123')
        self.profile = self.user.profile
        self.profile.user_type = 'freelancer'
        self.profile.save()
        
        self.service = Service.objects.create(
            freelancer=self.profile,
            title='Test Service',
            description='A test service',
            category='web_dev',
            price=100.00,
        )
    
    def test_service_creation(self):
        self.assertEqual(self.service.title, 'Test Service')
        self.assertEqual(self.service.price, 100.00)

class BookingTestCase(TestCase):
    def setUp(self):
        self.freelancer_user = User.objects.create_user(username='freelancer', password='pass123')
        self.client_user = User.objects.create_user(username='client', password='pass123')
        
        self.freelancer = self.freelancer_user.profile
        self.freelancer.user_type = 'freelancer'
        self.freelancer.save()
        
        self.client = self.client_user.profile
        self.client.user_type = 'client'
        self.client.save()
        
        self.service = Service.objects.create(
            freelancer=self.freelancer,
            title='Test Service',
            description='A test service',
            category='web_dev',
            price=100.00,
        )
    
    def test_booking_creation(self):
        booking = Booking.objects.create(
            service=self.service,
            client=self.client,
            freelancer=self.freelancer,
            total_price=100.00,
        )
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.total_price, 100.00)
