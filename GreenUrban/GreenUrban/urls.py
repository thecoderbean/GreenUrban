from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webstore.urls')),  
    path('retailer_login/', include('retailer.urls')),
    path('delivery_login/', include('delivery.urls')),
]