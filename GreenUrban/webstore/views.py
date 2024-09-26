from django.core.mail import send_mail
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import RegisteredUser
from retailer.models import Product, ProductImage, ProductReview, Favorite, Order
from .forms import ProfilePictureForm, ProfileUpdateForm, RegistrationForm, LoginForm
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ScrapForm

def index(request):
    return render(request, 'index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopping.html', {'products': products})

def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    images = ProductImage.objects.filter(product=product)
    reviews = ProductReview.objects.filter(product=product).order_by('-rating')
    total_images = images.count()
    
    total_reviews = reviews.count()
    ratings_distribution = reviews.values('rating').annotate(count=Count('rating')).order_by('-rating')
    ratings_percentage = {rating['rating']: (rating['count'] / total_reviews) * 100 for rating in ratings_distribution}

    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id).order_by('-rating')[:6]

    return render(request, 'view_product.html', {
        'product': product,
        'images': images,
        'reviews': reviews,
        'total_images': total_images,
        'similar_products': similar_products,
        'ratings_distribution': ratings_percentage
    })
    
def shopping(request):
    return render(request, 'shopping.html')

def about(request):
    return render(request, 'about.html')

def scrap(request):
    return render(request, 'scrap.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

@login_required
def account(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-order_date')
    return render(request, 'account.html', {'user_data': user, 'orders': orders})

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user_data': request.user})
    else:
        return redirect('login_view')

def pic_upload(request):
    if request.user.is_authenticated:
        user_data = request.user

        if request.method == 'POST':
            form = ProfilePictureForm(request.POST, request.FILES, instance=user_data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Image uploaded successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Image upload failed. Please check the form.')

        return render(request, 'home.html', {'user_data': user_data})
    else:
        return redirect('login_view')
    
def profile_update(request):
    if request.user.is_authenticated:
        user_data = request.user

        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user_data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('account')

        form = ProfileUpdateForm(instance=user_data)
        return render(request, 'account.html', {'form': form, 'user_data': user_data})
    else:
        return redirect('login_view')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration_data = form.cleaned_data
            registered_user = RegisteredUser(
                name=registration_data['name'],
                email=registration_data['email'],
                username=registration_data['username'],
                pincode=registration_data['pincode'],
                number=registration_data['number'],
                address=registration_data['address'],
            )
            registered_user.set_password(registration_data['password'])
            registered_user.save()
            messages.success(request, 'User registered successfully. Please login!')
            return redirect('login_view')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('index')

def shop_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query) | 
            Q(price__icontains=query) | 
            Q(available__icontains=query)
        )

    return render(request, 'shop.html', {'products': products})

def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect(request,'view_product', id=product_id)

def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'view_favorites.html', {'favorites': favorites})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock >= quantity:
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
            shipping_address=request.user.address,
        )
        product.stock -= quantity
        product.save()
        return redirect('cart')
    else:
        return redirect('product_detail', product_id=product_id)

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock >= quantity:
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
            shipping_address=request.user.address,
            status=1,
            delivery_boy_id=None,
        )
        product.stock -= quantity
        product.save()
        return redirect('order_summary', order_id=order.id)
    else:
        return redirect('product_detail', product_id=product_id)
    
@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = order.user
    return render(request, 'order_summary.html', {'order': order, 'user': user})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status not in [5, 4]: 
        order.status = 0  
        order.save()
    return redirect('order_summary', order_id=order_id)

def upload_scrap(request):
    if request.method == "POST":
        form = ScrapForm(request.POST, request.FILES)
        if form.is_valid():
            scrap = form.save(commit=False)
            scrap.user = request.user
            scrap.save()
            messages.success(request, 'Scrap uploaded successfully! Our pickup team will contact you when the pickup is scheduled.')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = ScrapForm()

    return render(request, 'scrap.html', {'form': form})
