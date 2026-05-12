from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category, Order, OrderItem


# ===== HOMEPAGE =====
def home(request):
    featured = Product.objects.filter(stock__gt=0)[:4]
    categories = Category.objects.all()
    context = {
        'page_title': 'Welcome',
        'featured': featured,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


# ===== PRODUCTS LIST =====
def products(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        all_products = all_products.filter(category=active_category)

    if search_query:
        all_products = all_products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'products': all_products,
        'categories': categories,
        'active_category': active_category,
        'search_query': search_query,
        'page_title': 'Shop',
    }
    return render(request, 'store/products.html', context)


# ===== PRODUCT DETAIL =====
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related': related,
        'page_title': product.name,
    }
    return render(request, 'store/product_detail.html', context)


# ===== ADD TO CART =====
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', {})
        key = str(product_id)

        if key in cart:
            cart[key]['quantity'] += quantity
        else:
            cart[key] = {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'image': product.image,
                'quantity': quantity,
            }

        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'"{product.name}" added to cart.')

    next_url = request.POST.get('next', 'store:products')
    return redirect(next_url)


# ===== CART =====
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = list(cart.values())
    for item in cart_items:
        item['subtotal'] = item['price'] * item['quantity']
    total_price = sum(item['subtotal'] for item in cart_items)
    total_items = sum(item['quantity'] for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
        'page_title': 'Cart',
    }
    return render(request, 'store/cart.html', context)


# ===== UPDATE CART QUANTITY =====
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        key = str(product_id)
        action = request.POST.get('action')

        if key in cart:
            if action == 'increase':
                cart[key]['quantity'] += 1
            elif action == 'decrease':
                if cart[key]['quantity'] > 1:
                    cart[key]['quantity'] -= 1
                else:
                    del cart[key]
            elif action == 'remove':
                del cart[key]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('store:cart')


# ===== REMOVE FROM CART (legacy) =====
def remove_from_cart(request, item_index):
    cart = request.session.get('cart', {})
    keys = list(cart.keys())
    if 0 <= item_index < len(keys):
        del cart[keys[item_index]]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('store:cart')


# ===== CHECKOUT =====
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:cart')

    cart_items = list(cart.values())
    for item in cart_items:
        item['subtotal'] = item['price'] * item['quantity']
    total_price = sum(item['subtotal'] for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if not (name and email and address):
            messages.error(request, 'Please fill in all fields.')
        else:
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                address=address,
                total_price=total_price,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    product_price=item['price'],
                    quantity=item['quantity'],
                )

            request.session['cart'] = {}
            request.session['last_order_id'] = order.id
            request.session.modified = True

            return redirect('store:order_success')

    initial = {}
    if request.user.is_authenticated:
        initial['name'] = request.user.get_full_name() or request.user.username
        initial['email'] = request.user.email

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'initial': initial,
        'page_title': 'Checkout',
    }
    return render(request, 'store/checkout.html', context)


# ===== ORDER SUCCESS =====
def order_success(request):
    order_id = request.session.get('last_order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.prefetch_related('items').get(id=order_id)
        except Order.DoesNotExist:
            pass

    context = {
        'order': order,
        'page_title': 'Order Confirmed',
    }
    return render(request, 'store/order_success.html', context)


# ===== REGISTER =====
def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not all([username, email, password1, password2]):
            messages.error(request, 'Please fill in all required fields.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.username}!')
            return redirect('store:home')

    context = {'page_title': 'Create Account'}
    return render(request, 'store/register.html', context)


# ===== LOGIN =====
def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.POST.get('next') or 'store:home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    context = {'page_title': 'Sign In'}
    return render(request, 'store/login.html', context)


# ===== LOGOUT =====
def logout_view(request):
    logout(request)
    return redirect('store:home')


# ===== PROFILE =====
@login_required(login_url='store:login')
def profile(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    context = {
        'orders': orders,
        'page_title': 'My Account',
    }
    return render(request, 'store/profile.html', context)
