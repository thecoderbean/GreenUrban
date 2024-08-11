from django.urls import path
from .views import RetailerLoginView, retailer_dashboard, logout_user, profile , add_product, edit_product, delete_product, orders, generate_qr_code, update_order_status

urlpatterns = [
    path('', RetailerLoginView.as_view(), name='retailer_login'),
    path('login/', RetailerLoginView.as_view(), name='retailer_login'),
    path('dashboard/', retailer_dashboard, name='retailer_dashboard'),
    path('profile/', profile, name='profile'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:pk>/', edit_product, name='edit_product'),
    path('orders/', orders, name='orders'),
    path('delete_product/<int:pk>/', delete_product, name='delete_product'),
    path('logout/', logout_user, name='logout'),
    path('generate_qr_code/<int:order_id>/', generate_qr_code, name='generate_qr_code'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
]
