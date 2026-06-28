from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import HttpResponseForbidden
from .models import UserProfile, Service, Booking, Review
from .forms import UserRegisterForm, UserProfileForm, ServiceForm, BookingForm, ReviewForm

# ===== MAIN VIEWS =====
def home(request):
    services = []
    
    # Check if Flask forwarded a Firebase idToken in the URL query parameters
    token = request.GET.get('token')
    
    if token:
        try:
            #  verify the token by calling the Flask API profile endpoint
            headers = {'Authorization': f'Bearer {token}'}
            profile_response = requests.get("http://127.0.0.1:5000/api/profile", headers=headers, timeout=5)
            
            if profile_response.status_code == 200:
                firebase_user = profile_response.json()
                # If your format_response wraps data in a 'data' key, adjust this line:
                # firebase_user = firebase_user.get('data', firebase_user)
                
                email = firebase_user.get('email')
                
                if email:
                    # Get or create the matching local Django User instance
                    username = email.split('@')[0]
                    user_obj, created = User.objects.get_or_create(
                        username=username, 
                        defaults={'email': email}
                    )
                    
                    # Force log the user into the current Django session
                    login(request, user_obj)
                    
                    # Ensure their UserProfile profile table exists
                    UserProfile.objects.get_or_create(user=user_obj)
                    
        except Exception as auth_err:
            print("AUTOMATIC AUTH ERROR IN DJANGO:", auth_err)

    #  Fetch the external marketplace services from Flask API as usual
    try:
        response = requests.get(
            "http://127.0.0.1:5000/api/services",
            timeout=5
        )
        response.raise_for_status()
        services = response.json()
        print("SERVICES:", services)  
        
    except Exception as e:
        print("API SERVICES FETCH ERROR:", e)

    return render(request, "home.html", {"services": services})
# ===== SERVICE VIEWS =====
def service_list(request):
    services = Service.objects.filter(status='active')

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        services = services.filter(category=category)
    if search:
        services = services.filter(Q(title__icontains=search) | Q(description__icontains=search))

    return render(request, 'service_list.html', {'services': services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})


@login_required
def create_service(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if profile.user_type != 'freelancer':
        return HttpResponseForbidden("Only freelancers")

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.freelancer = profile
            service.save()
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm()

    return render(request, 'service_form.html', {'form': form})



def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)

    return render(request, 'profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=request.user.pk)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile_form.html', {'form': form})


@login_required
def booking_list(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    bookings = Booking.objects.filter(client=profile) | Booking.objects.filter(freelancer=profile)

    return render(request, 'booking_list.html', {'bookings': bookings})


@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking.objects.create(
                service=service,
                client=profile,
                freelancer=service.freelancer,
                total_price=service.price
            )
            return redirect('booking_list')
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if booking.client != profile and booking.freelancer != profile:
        return HttpResponseForbidden()

    booking.status = 'cancelled'
    booking.save()

    return redirect('booking_list')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)

            if user:
                login(request, user)

                # 🔥 FIX IMPORTANT
                UserProfile.objects.get_or_create(user=user)

                return redirect('home')
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def external_services(request):
    try:
        response = requests.get("http://127.0.0.1:5000/api/services")
        services = response.json()
    except:
        services = []

    return render(request, "service_list.html", {"services": services})

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if service.freelancer != profile:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)

    return render(request, 'service_form.html', {'form': form})


@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if service.freelancer != profile:
        return HttpResponseForbidden()

    service.delete()
    return redirect('service_list')



@login_required
def create_review(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if booking.client != profile:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.reviewer = request.user
            review.save()

            booking.status = 'completed'
            booking.save()

            return redirect('booking_list')
    else:
        form = ReviewForm()

    return render(request, 'review_form.html', {'form': form})