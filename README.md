
# User Profile Management System

---

## Features

1. **User Registration**
   - Users can register by providing their username, email, password, address, phone number, and name.
   - Validation for phone number (10-digit) and email format.

2. **User Login**
   - Users can log in using their credentials.
   - Incorrect username or password results in an error message.

3. **User Dashboard**
   - A protected dashboard page accessible only to logged-in users.

4. **Profile Management**
   - Users can edit their profiles, including updating their username, email, address, phone number, and name.
   - Validations are applied to ensure correct input.

5. **Logout**
   - Users can log out, and their session will be cleared.

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Django 4.0+

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/muhammedshabeen/user-management-mixins.git
   cd user-management-mixins
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL Database**

   - Create a PostgreSQL database.
   - Update the `DATABASES` setting in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': '<your_database_name>',
             'USER': '<your_database_user>',
             'PASSWORD': '<your_database_password>',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Run Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**

   - Open `http://127.0.0.1:8000/` in your browser.

---

## File Structure

### URLs Configuration

```python
from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('user-login', UserLoginView.as_view(), name='user_login'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('signout', SignOutView.as_view(), name='signout'),
    path('profile', ProfileView.as_view(), name='profile'),
]
```

### Views

- **Register**: Handles user registration with form validation.
- **Login**: Authenticates users and redirects to the dashboard.
- **Dashboard**: Displays the user's dashboard.
- **Profile**: Allows users to edit their profiles.
- **Logout**: Logs out the user and clears the session.

---

## Forms

### Registration Form
Handles user registration with validations for phone number, email, and passwords.

### Profile Edit Form
Handles profile editing with field validations.

---

## Database

The project uses **PostgreSQL** as the database backend.

- To set up the database, ensure you update the `DATABASES` setting in `settings.py`.
- Use `python manage.py migrate` to create the required tables.

---

## Views Implementation with Mixins and Generic API Views

In this project, **mixins** and **generic views** are used to manage views for registration, login, dashboard, profile management, and logout. Here is an overview of how they are implemented:

### Register View (Registration)

Uses Django's **CreateView** to handle the user registration form. The form is validated, and upon successful registration, the user is redirected to the login page.

```python
class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful")
        return response
```

### User Login View

Uses **FormView** to handle user authentication. The form is validated, and if successful, the user is logged in and redirected to the dashboard.

```python
class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Login successful")
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
```

### Dashboard View

Uses **LoginRequiredMixin** and **TemplateView** to ensure that only authenticated users can access the dashboard.

```python
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
```

### Profile Edit View

Uses **LoginRequiredMixin** and **UpdateView** to allow users to edit their profiles. Only the logged-in user can edit their own profile.

```python
class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
```

### Sign Out View

Uses **LoginRequiredMixin** and **TemplateView** to log out the user and clear their session.

```python
class SignOutView(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('user_login')
```

---

This approach uses Django's **generic views** and **mixins** to handle common user management operations, allowing for clean and maintainable code.
