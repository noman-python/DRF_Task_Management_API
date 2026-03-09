from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user_app.Api import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('api/token/', TokenRefreshView.as_view(), name='token_refresh'),
]