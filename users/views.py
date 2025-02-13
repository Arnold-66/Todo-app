from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)

def register(request):
    print("Request method:", request.method)  # Add this line to check request method

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid, saving user...")
            user = form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')  # Redirect to login page after success
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})



def custom_logout(request):
    logger.debug("Custom logout called.")
    logout(request)  
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect instead of render

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Successfully logged in!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('tasklist')  # Ensure 'tasklist' exists in urls.py


