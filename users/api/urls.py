from django.urls import path
from .views import UserProfileListCreateView, CustomTokenObtainPairView

urlpatterns = [
    path("register/", UserProfileListCreateView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
]
