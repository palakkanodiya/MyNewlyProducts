from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
    


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/create/', ProductView.as_view(), name='product_create'),
    path('buyer/', ProductListView.as_view(), name='product_list'),
    path('current/', SellerProductListView.as_view(), name='seller_product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]




































































# RegisterView, LoginView, ProductView, ProductListView,SellerProductListView, ProductDetailView