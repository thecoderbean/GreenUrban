from django.urls import reverse_lazy
from django.views.generic import View
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import RetailerLoginForm,ProductForm, ProductImageFormSet,ProductImage
from .models import Retailer,Order
from .models import Product
from django.db.models import Q
from django.http import HttpResponse
import qrcode
from io import BytesIO

class RetailerLoginView(LoginView):
    form_class = RetailerLoginForm
    template_name = 'retailer/retailer_login.html'
    success_url = reverse_lazy('retailer_dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Login successful.')
        return redirect(self.get_success_url())
    
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.retailer = request.user.retailer  # Set the retailer to the current user
            product.save()
            for form in formset:
                if form.cleaned_data:
                    image = form.save(commit=False)
                    image.product = product
                    image.save()
            return redirect('retailer_dashboard')
    else:
        product_form = ProductForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())

    products = Product.objects.filter(retailer=request.user.retailer)
    return render(request, 'retailer/add_product.html', {'product_form': product_form, 'formset': formset, 'products': products})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if product_form.is_valid() and formset.is_valid():
            product_form.save()
            formset.save()
            return redirect('add_product')  # Redirect to the add_product page
    else:
        product_form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    return render(request, 'retailer/edit_product.html', {'product_form': product_form, 'formset': formset})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('add_product')  # Redirect to the add_product page
    return render(request, 'retailer/confirm_delete.html', {'product': product})

 
@login_required
def retailer_dashboard(request):
    return render(request,'retailer/retailer_index.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('retailer_login')

@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'retailer/retailer_dashboard.html', {'user_data': request.user})
    else:
        return redirect('retailer_login')
    
@login_required
def profile(request):
    try:
        retailer = Retailer.objects.get(user=request.user)
    except Retailer.DoesNotExist:
        messages.error(request, "Retailer profile does not exist.")
        return redirect('retailer_login')
    return render(request, 'retailer/retailer_profile.html', {'retailer': retailer})


@login_required
def orders(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    user = request.user
    
    # Get the Retailer instance associated with the logged-in user
    try:
        retailer = Retailer.objects.get(user=user)
    except Retailer.DoesNotExist:
        # Handle the case where the logged-in user is not a retailer
        context = {
            'orders': [],
            'error': 'You are not authorized to view this page.',
        }
        return render(request, 'orders.html', context)
    
    # Filter orders where the product's retailer ID matches the logged-in user's ID
    orders = Order.objects.filter(product__retailer=retailer)

    if query:
        orders = orders.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__number__icontains=query) |
            Q(id__icontains=query) |
            Q(user__address__icontains=query)
        )
        
    if start_date and end_date:
        orders = orders.filter(order_date__range=[start_date, end_date])
        
    context = {
        'orders': orders,
    }
    
    return render(request, 'retailer/orders.html', context)

def generate_qr_code(request, order_id):
    # Generate QR code for the order ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(order_id)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status_str = request.POST.get('status')
        try:
            status = int(status_str)
        except ValueError:
            status = 2
        order.status = status
        order.save()
    return redirect('orders')