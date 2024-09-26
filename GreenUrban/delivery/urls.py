from django.urls import path
from .views import DeliveryBoyLoginView, DeliveryBoyLogoutView, DeliveryDashboardView,order_dispatch, pickup_view, scan_qr_code, order_details, mark_as_out_for_delivery, start_qr_scanner, out_to_deliver, mark_as_delivered, out_for_delivery_orders,user_detail

urlpatterns = [
    path('', DeliveryBoyLoginView.as_view(), name='delivery_boy_login'),
    path('logout/', DeliveryBoyLogoutView.as_view(), name='delivery_boy_logout'),
    path('dashboard/', DeliveryDashboardView.as_view(), name='delivery_dashboard'),
    path('order_dispatch/', order_dispatch, name='order_dispatch'),
    path('out_to_deliver/', order_dispatch, name='out_to_deliver'),
    path('delivered/', order_dispatch, name='delivered'),
    path('pickupview/', pickup_view, name='pickupview'),
    path('user_detail/<int:user_id>/', user_detail, name='user_detail'),
    path('scan_qr_code/', scan_qr_code, name='scan_qr_code'),
    path('start_qr_scanner/', start_qr_scanner, name='start_qr_scanner'),
    path('order_details/<int:order_id>/', order_details, name='order_details'),
    path('mark_as_out_for_delivery/<int:order_id>/', mark_as_out_for_delivery, name='mark_as_out_for_delivery'),
    path('deliver/', out_to_deliver, name='deliver'),
    path('order/<int:order_id>/out_for_delivery/', mark_as_out_for_delivery, name='mark_as_out_for_delivery'),
    path('order/<int:order_id>/delivered/', mark_as_delivered, name='mark_as_delivered'),
    path('out_for_delivery/', out_for_delivery_orders, name='out_for_delivery_orders'),
    path('order/<int:order_id>/delivered/', mark_as_delivered, name='mark_as_delivered'),
]
