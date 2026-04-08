from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import CustomUser


def home_view(request):
    if request.user.is_authenticated:
        return redirect("sample_dashboard")
    return redirect("sample_login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("sample_dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        company_name = request.POST.get("company_name", "").strip()
        department_code = request.POST.get("department_code", "").strip()

        if not email or not password or not company_name or not department_code:
            messages.error(request, "All fields are required.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            CustomUser.objects.create_user(
                email=email,
                password=password,
                company_name=company_name,
                department_code=department_code,
            )
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("sample_login")

    return render(request, "users/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("sample_dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
        else:
            login(request, user)
            return redirect("sample_dashboard")

    return render(request, "users/login.html")


@login_required(login_url="sample_login")
def dashboard_view(request):
    return render(request, "users/dashboard.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("sample_login")
