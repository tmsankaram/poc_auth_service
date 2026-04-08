from django.urls import path

from .views import dashboard_view, home_view, login_view, logout_view, register_view

urlpatterns = [
    path("", home_view, name="sample_home"),
    path("login/", login_view, name="sample_login"),
    path("register/", register_view, name="sample_register"),
    path("dashboard/", dashboard_view, name="sample_dashboard"),
    path("logout/", logout_view, name="sample_logout"),
]
