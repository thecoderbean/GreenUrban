from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import DeliveryBoyLoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from retailer.models import Order
import cv2
from django.middleware.csrf import get_token
from pyzbar import pyzbar
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from webstore.models import Scrap  # Import your Scrap model
from webstore.models import RegisteredUser  # Import your RegisteredUser model



class DeliveryBoyLoginView(LoginView):
    form_class = DeliveryBoyLoginForm
    template_name = 'delivery/index.html'

    def get_success_url(self):
        return reverse_lazy('delivery_dashboard')

    def form_valid(self, form):
        user = form.get_user()
        if hasattr(user, 'deliveryboy'):
            login(self.request, user)
            messages.success(self.request, 'Login successful.')
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, 'Invalid login credentials.')
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class DeliveryBoyLogoutView(LogoutView):
    next_page = reverse_lazy('delivery_boy_login')

@method_decorator(login_required, name='dispatch')
class DeliveryDashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'delivery/dashboard.html')

@login_required
def order_dispatch(request):
    return render(request, 'delivery/order_dispatch.html')

@login_required
def pickup_view(request):
    # Query all scrap items
    scrap_items = Scrap.objects.select_related('user').all()  # Ensure related user is fetched

    # Pass scrap items to the template
    return render(request, 'delivery/pickupview.html', {'scrap_items': scrap_items})

def user_detail(request, user_id):
    
    user = get_object_or_404(RegisteredUser, id=user_id)
    return render(request, 'delivery/user_detail.html', {'user': user})

@login_required
def scan_qr_code(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.status = 3  # Dispatched
        order.delivery_boy_id = request.user.id  # Assign delivery boy
        order.save()
        return redirect('order_details', order_id=order_id)
    return render(request, 'delivery/scan_qr_code.html')

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'delivery/order_details.html', {'order': order})

@login_required
def mark_as_out_for_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 4  # Out for Delivery
    order.save()
    return redirect('order_details', order_id=order_id)

@login_required
def dispatched_orders(request):
    orders = Order.objects.filter(delivery_boy_id=request.user.id, status=3)
    return render(request, 'delivery/dispatched_orders.html', {'orders': orders})

@login_required
@csrf_exempt
def start_qr_scanner(request):
    cap = cv2.VideoCapture(0)
    order_id = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            order_id = obj.data.decode("utf-8")
            print(f"Order ID: {order_id}")

            # Draw a rectangle around the QR code
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, order_id, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Stop the camera once a QR code is detected
            cap.release()
            cv2.destroyAllWindows()

            # Call a function to update the order status
            delivery_boy_id = request.user.id  # Use the logged-in user's ID
            response = update_order_status(order_id, delivery_boy_id, 3)

            return JsonResponse(response)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return JsonResponse({'message': 'QR scanner stopped'})

@login_required
@csrf_exempt
def start_delivery_qr_scanner(request):
    cap = cv2.VideoCapture(0)
    order_id = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            order_id = obj.data.decode("utf-8")
            print(f"Order ID: {order_id}")

            # Draw a rectangle around the QR code
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, order_id, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Stop the camera once a QR code is detected
            cap.release()
            cv2.destroyAllWindows()

            # Call a function to update the order status
            delivery_boy_id = request.user.id  # Use the logged-in user's ID
            response = update_order_status(order_id, delivery_boy_id, 5)

            return JsonResponse(response)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return JsonResponse({'message': 'QR scanner stopped'})

def update_order_status(order_id, delivery_boy_id, status):
    try:
        order = get_object_or_404(Order, id=order_id)
        order.status = status  # Update status
        order.delivery_boy_id = delivery_boy_id  # Assign delivery boy
        order.save()
        return {'message': f'Order {order_id} status updated to {status} successfully'}
    except Exception as e:
        print(f"Error updating order status: {e}")
        return {'error': f'Error updating order {order_id}: {str(e)}'}
    

@login_required
def out_to_deliver(request):
    delivery_boy_id = request.user.id
    # Fetch orders with status 'Dispatched' (status = 3) and assigned to the current delivery boy
    orders = Order.objects.filter(status=3, delivery_boy_id=delivery_boy_id)

    return render(request, 'delivery/out_to_deliver.html', {'orders': orders})

@login_required
def mark_as_out_for_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 3:  # Ensure it's in the 'Dispatched' state before updating
        order.status = 4  # Out for Delivery
        order.save()
    return redirect('order_details', order_id=order_id)

@login_required
def mark_as_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 4:  # Ensure it's 'Out for Delivery' before marking it as delivered
        order.status = 5  # Delivered
        order.save()
    return redirect('order_details', order_id=order_id)

@login_required
def out_for_delivery_orders(request):
    # Get all orders that are out for delivery (status = 4)
    orders = Order.objects.filter(status=4)
    context = {
        'orders': orders
    }
    return render(request, 'delivery/deliver.html', context)

@login_required
def mark_as_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 4:  # Ensure it's 'Out for Delivery' before marking it as delivered
        order.status = 5  # Delivered
        order.save()
    return redirect('out_for_delivery_orders')