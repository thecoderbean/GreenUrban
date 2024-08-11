from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login_view', views.login_view, name='login_view'),
    path('register_view', views.register_view, name='register_view'),
    path('home', views.home, name='home'),
    path('account', views.account, name='account'),
    path('register_user', views.register_user, name='register_user'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('pic_upload', views.pic_upload, name='pic_upload'),
    path('shopping/', views.product_list, name='shopping'),
    path('scrap/', views.scrap, name='scrap'),
    path('sewage/', views.product_list, name='sewage'),
    path('land/', views.product_list, name='land'),
    path('shop_products', views.shop_products, name='shop_products'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('products/<int:id>/', views.view_product, name='view_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('profile_upload', views.profile_update, name='profile_upload'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('retailer_login/', include('retailer.urls')),
    path('delivery_login/', include('delivery.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    