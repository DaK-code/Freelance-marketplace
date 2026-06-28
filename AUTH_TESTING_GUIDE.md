# Django Authentication - Testing Guide

## Quick Test Instructions

### **Setup (First Time)**

```bash
cd django_app
python manage.py migrate
python manage.py createsuperuser
# Create admin account: admin / admin1234
python manage.py runserver
```

---

## Test Scenarios

### **Test 1: User Registration**

**Steps:**
1. Open: http://localhost:8000/register/
2. Fill form with:
   ```
   First Name: Alice
   Last Name: Johnson
   Username: alice_j
   Email: alice@example.com
   Password: testpass123
   Confirm: testpass123
   ```
3. Click "Create Account"

**Expected Results:**
-  Success message: "Registration successful! Please login."
-  Redirected to login page
-  User created in database
-  UserProfile auto-created

**Validation Test:**
- Try same email again → "This email is already registered."
- Try same username again → "This username is already taken."
- Try mismatched passwords → "Passwords do not match."

---

### **Test 2: User Login**

**Steps:**
1. Go to: http://localhost:8000/login/
2. Enter:
   ```
   Email: alice@example.com
   Password: testpass123
   ```
3. Click "Login"

**Expected Results:**
-  Success message: "Welcome back, Alice Johnson!"
-  Redirected to home page
-  Navbar shows user dropdown
-  Session created

**Error Tests:**
- Wrong email → "User not found."
- Right email, wrong password → "Invalid password."

---


**Error Tests:**
- Wrong current password → "Old password is incorrect."
- Mismatched new passwords → "Passwords do not match."

---

### **Test 3: Navigation Links**

**Unauthenticated User:**
- Navbar shows: "Login" and "Register"
- Click Login → /login/
- Click Register → /register/

**Authenticated User:**
- Navbar shows user dropdown with name
- Dropdown includes:
  - "My Profile"
  - "Edit Profile"
  - "Change Password"
  - "Logout"

**Admin User:**
- Same as authenticated
- Plus "Admin Panel" in dropdown

---

### **Test 4: Profile Integration**

**Steps:**
1. Register new user (alice@example.com)
2. Go to admin: http://localhost:8000/admin/
3. Users → select "alice_j"
4. Check related UserProfile

**Expected Results:**
-  serProfile exists
-  user_type = "freelancer" (default)
-  rating = 0.0 (default)
-  is_verified = False (default)

---

### **Test 5: Logout**

**Steps:**
1. Login to account
2. Click dropdown → "Logout"
3. Go to: http://localhost:8000/logout/

**Expected Results:**
-  Success message: "Logged out successfully."
-  Redirected to home
-  Navbar no longer shows user dropdown
-  Session cleared

---

### **Test 6: Login Required Pages**

**Steps:**
1. Logout (if logged in)


**Expected Results:**
-  Redirected to login page
-  After login, returns to password-change page

---

### **Test 7: Edit Profile** (Verify Integration)

**Steps:**
1. Login as user
2. Click "My Profile" → "Edit Profile"
3. Go to: http://localhost:8000/profile/edit/
4. Change: Bio, hourly rate, etc.
5. Click Save

**Expected Results:**
-  Profile updated
-  Changes reflected in /profile/<id>/
-  New data appears in admin

---

### **Test 8: Database Verification**

**Via Django Shell:**
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from marketplace.models import UserProfile

# Check user
user = User.objects.get(username='alice_j')
print(user.email)  # alice@example.com
print(user.password)  # Should be hashed, not plaintext

# Check profile auto-created
profile = user.profile
print(profile.user_type)  # freelancer
print(profile.rating)  # 0.0
```

---



### **Test Email Validation:**
```bash
# In registration form
- Email: alice@example.com → Valid
- Email: not-an-email → Invalid
- Email: alice@example.com (second time) → "Already registered"
```

### **Test Username Validation:**
```bash
# In registration form
- Username: alice_j → Valid
- Username: a → Valid (Django allows)
- Username: alice_j (second time) → "Already taken"
```

### **Test Password Requirements:**
```bash
# Minimum 6 characters
- "pass" → Too short (if enforced in JS)
- "pass12" → Valid
- "password123" → Valid
```

---

