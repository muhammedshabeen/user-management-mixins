from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.contrib.auth import logout
from .models import *
from .forms import RegistrationForm, ProfileEditForm

# Handles user registration
class RegisterView(CreateView):
    template_name = 'register.html' # Template for rendering the registration form
    form_class = RegistrationForm   # Form class used for user registration
    success_url = reverse_lazy('user_login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        # Save the form data to create a new user
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful")
        return response

    def form_invalid(self, form):
        # Handle form errors and display messages for each invalid field
        response = super().form_invalid(form)
        for field_name, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field_name}: {error}")
        return response


# Handles user login
class UserLoginView(FormView):
    template_name = 'login.html' # Template for rendering the login form
    form_class = AuthenticationForm # Form class used for user authentication
    success_url = reverse_lazy('dashboard')  # Redirect to dashboard page after successful login

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        # checking the user with username and password exists
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            # Authenticate and log in the user
            login(self.request, user)
            messages.success(self.request, "Login successful")
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
    
    def form_invalid(self, form):
        # Add a general error message for invalid form submissions
        messages.error(self.request, "Login failed. Please check your credentials.")
        return super().form_invalid(form)


# Displays the dashboard page (only accessible to logged-in users)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


# Allows users to view and update their profile (only accessible to logged-in users)
class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user  # Fetch the current logged-in user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile Updated")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field_name, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field_name}: {error}")
        return response


# Logs out the user and clears the session (only accessible to logged-in users)
class SignOutView(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('user_login')
