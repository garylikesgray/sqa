from django.shortcuts import render, redirect, get_object_or_404

from .models import Product


# ===== VIEW 1: HOMEPAGE =====
def home(request):
    """
    Show the homepage with a welcome message.
    """
    context = {
        'page_title': 'Welcome to Makeup Store',
    }
    return render(request, 'store/home.html', context)


# ===== VIEW 2: PRODUCT LIST PAGE =====
def products(request):
    """
    Show all products in a grid.

    Important: this page must use the database (Django model),
    so products added from Django Admin show up here.
    """
    context = {
        'products': Product.objects.all(),
        'page_title': 'Our Products',
    }
    return render(request, 'store/products.html', context)


# ===== VIEW 3: ADD TO CART =====
def add_to_cart(request, product_id):
    """
    Add a product to the cart using Django sessions.
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        # Create a cart in the session if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = []

        # Add the product to the cart
        request.session['cart'].append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image,
        })

        request.session.modified = True

    # Send user back to products page
    return redirect('store:products')


# ===== VIEW 4: SHOW CART PAGE =====
def cart(request):
    """
    Show the shopping cart with all added items.
    Calculate the total price.
    """
    # Get cart from session (or empty list if no cart)
    cart_items = request.session.get('cart', [])

    # Calculate total price
    total_price = sum(item['price'] for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'page_title': 'Shopping Cart',
    }
    return render(request, 'store/cart.html', context)


# ===== VIEW 5: REMOVE FROM CART =====
def remove_from_cart(request, item_index):
    """
    Remove a specific item from the cart.
    """
    # Get cart from session
    cart = request.session.get('cart', [])

    # Remove the item if the index is valid
    if 0 <= item_index < len(cart):
        cart.pop(item_index)

    # Save the session
    request.session.modified = True

    # Send user back to cart page
    return redirect('store:cart')


# ===== VIEW 6: CHECKOUT PAGE =====
def checkout(request):
    """
    Show checkout form or process the form.
    """
    # If user submitted the form (POST)
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Save order info to session (we'll use it on success page)
        request.session['order'] = {
            'name': name,
            'email': email,
            'address': address,
        }
        request.session.modified = True

        # Clear the cart after checkout
        request.session['cart'] = []
        request.session.modified = True

        # Send user to success page
        return redirect('store:order_success')

    # If user just opened the page (GET)
    context = {
        'page_title': 'Checkout',
    }
    return render(request, 'store/checkout.html', context)


# ===== VIEW 7: ORDER SUCCESS PAGE =====
def order_success(request):
    """
    Show a success message after checkout.
    """
    # Get the order info from session
    order = request.session.get('order', {})

    context = {
        'order': order,
        'page_title': 'Order Successful',
    }
    return render(request, 'store/order_success.html', context)





