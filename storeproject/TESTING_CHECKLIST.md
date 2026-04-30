# 🧪 Testing Checklist - Makeup Store

## ✅ Test Each Feature

### 1. Homepage ✨
- [ ] Visit `http://127.0.0.1:8000/`
- [ ] See "Welcome to Makeup Store 💄"
- [ ] See "Discover our beautiful collection..." message
- [ ] Click "Shop Now" button → Goes to /products/

### 2. Products Page 🛍️
- [ ] Visit `http://127.0.0.1:8000/products/`
- [ ] See all 6 products in a nice grid
- [ ] Each product shows:
  - [ ] Emoji
  - [ ] Product name
  - [ ] Price
  - [ ] Description
  - [ ] "Add to Cart" button
- [ ] Products shown:
  1. 💄 Lipstick Classic - $12.99
  2. 🎨 Foundation Perfect - $18.99
  3. ✨ Mascara Lash - $15.99
  4. 🌸 Blush Glow - $11.99
  5. 👁️ Eyeshadow Palette - $24.99
  6. ✨ Lipgloss Shine - $9.99

### 3. Add to Cart 🛒
- [ ] Click "Add to Cart" for any product
- [ ] Page stays on products page
- [ ] No error messages
- [ ] Item actually added to cart

### 4. Shopping Cart Page 🛒
- [ ] Visit `http://127.0.0.1:8000/cart/`
- [ ] See all added items
- [ ] Each item shows:
  - [ ] Emoji + Product name
  - [ ] Price
  - [ ] Quantity: 1
  - [ ] Remove button
- [ ] See total price (sum of all items)
- [ ] See "Proceed to Checkout" button

### 5. Remove from Cart ❌
- [ ] Click "Remove" button on any item
- [ ] Item disappears from cart
- [ ] Total price updates
- [ ] Cart stays empty if all items removed

### 6. Empty Cart Message 📭
- [ ] Visit cart with no items
- [ ] See "Your cart is empty" message
- [ ] See "Continue Shopping" button
- [ ] Click "Continue Shopping" → Goes to products

### 7. Checkout Form 📝
- [ ] Visit `http://127.0.0.1:8000/checkout/`
- [ ] See form with fields:
  - [ ] Full Name (text input)
  - [ ] Email Address (email input)
  - [ ] Shipping Address (textarea)
- [ ] See "Complete Order" button
- [ ] All fields are required

### 8. Submit Order ✅
- [ ] Fill in all form fields:
  - Name: `John Doe`
  - Email: `john@example.com`
  - Address: `123 Main St, City, State 12345`
- [ ] Click "Complete Order"
- [ ] Goes to order success page

### 9. Order Success Page 🎉
- [ ] See "✨ Order Successful! ✨" message
- [ ] See customer name: `John Doe`
- [ ] See order details box with:
  - [ ] Email: `john@example.com`
  - [ ] Shipping Address: `123 Main St, City, State 12345`
- [ ] See "We'll send you a confirmation email shortly."
- [ ] See "Back to Home" button

### 10. Cart Cleared After Order 🧹
- [ ] After checkout, visit cart again
- [ ] Cart should be empty
- [ ] See "Your cart is empty" message

### 11. Navigation ✨
- [ ] Click "Home" link → Goes to /
- [ ] Click "Shop" link → Goes to /products/
- [ ] Click "Cart" link → Goes to /cart/
- [ ] Header appears on all pages
- [ ] Navigation works from every page

### 12. Design & Styling 🎨
- [ ] Colors are soft (pink, white, gray)
- [ ] No harsh colors
- [ ] Layout is centered and clean
- [ ] Text is readable
- [ ] Buttons look nice
- [ ] Forms are easy to use
- [ ] Works on different screen sizes

### 13. CSS Loading ✨
- [ ] All pages have proper styling
- [ ] No unstyled pages
- [ ] Colors match throughout
- [ ] Fonts are consistent

---

## 🐛 If Tests Fail

### Products not showing?
- Check `store/views.py` for `PRODUCTS` list
- Make sure `products.html` has `{% for product in products %}`

### Cart not saving items?
- Run: `python manage.py migrate`
- Check that session middleware is enabled in settings

### CSS not loading?
- In `base.html`, make sure you have:
  ```html
  {% load static %}
  <link rel="stylesheet" href="{% static 'store/style.css' %}">
  ```

### Forms not submitting?
- Check for `{% csrf_token %}` in the form
- Make sure form has `method="POST"`

### Redirects not working?
- Check URL names in `store/urls.py` match `{% url %}` tags in templates

---

## 📊 Test Results Summary

After testing everything above, you should be able to say:

✅ I can browse the store
✅ I can see all products
✅ I can add items to my cart
✅ I can see my cart total
✅ I can remove items
✅ I can fill out checkout form
✅ I see order confirmation
✅ The design looks beautiful
✅ Everything is working!

🎉 **Congratulations! Your app is production-ready!**
