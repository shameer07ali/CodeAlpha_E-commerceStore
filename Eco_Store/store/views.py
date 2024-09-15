from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile, Cart, CartItem, Order
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User 
from .forms import UserRegistrationForm, ProfileForm, ProductForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .forms import ProfileForm
from .models import Profile

def edit_profile(request):
    # Ensure the user has a profile
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user == product.user or request.user.is_staff:
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('home') 
    else:
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('product_detail', slug=slug)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Ensure the product is associated with the logged-in user
            # Ensure slug is unique
            if Product.objects.filter(slug=product.slug).exists():
                form.add_error('slug', 'This slug is already in use.')
            else:
                product.save()
                return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@login_required
def buy_now(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('checkout')

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            return add_to_cart(request, product.id)
        elif 'buy_now' in request.POST:
            return buy_now(request, product.id)

    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'store/edit_profile.html', {'form': form})

@login_required
def view_profile(request):
    return render(request, 'store/view_profile.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # or wherever you want to redirect
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid credentials'})
    return render(request, 'store/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None
    
    return render(request, 'store/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

# for order processing 
@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.cartitem_set.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('cart_detail')
    except Cart.DoesNotExist:
        messages.error(request, "No cart found.")
        return redirect('home')
    
    order = Order.objects.create(user=request.user, cart=cart, total_price=cart.get_total())
    return render(request, 'store/checkout.html', {'order': order})

