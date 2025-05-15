from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
def home(request):
    return render(request, 'home.html')

 # Assuming your HTML file is named landing.html
from django.shortcuts import render

def about(request):
    return render(request, 'about.html')
def news(request):
    return render(request, 'news.html')
def blog(request):
    return render(request, 'blog.html')
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Or 'home' or 'landing_page'



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Superuser -> Admin dashboard
            else:
                return redirect('home')  # Normal user -> User dashboard
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib import messages

User = get_user_model()

import random
import string

def generate_random_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail

User = get_user_model()

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

        password = generate_random_password()

        user = User(
            first_name=fname,
            last_name=lname,
            username=username,
            email=email,
            phone_number=phone,
            address=address,
            profile_image=profile_image,
            password=make_password(password)
        )
        user.save()

        send_mail(
            subject='Welcome to Our eCommerce Platform',
            message=f'Hi {fname},\n\nYour account has been created.\nUsername: {username}\nPassword: {password}',
            from_email='noreply@ecommerce.com',
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Registration successful. Check your email for login details.")
        return redirect('login')
    return render(request, 'register.html')

from django.http import JsonResponse
import re

def validate_field(request):
    field = request.GET.get('field')
    value = request.GET.get('value')

    if field == 'username':
        if User.objects.filter(username=value).exists():
            return JsonResponse({'valid': False, 'message': 'Username already exists.'})
        return JsonResponse({'valid': True})

    if field == 'email':
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value) or not value.endswith(".com"):
            return JsonResponse({'valid': False, 'message': 'Enter a valid .com email.'})
        if User.objects.filter(email=value).exists():
            return JsonResponse({'valid': False, 'message': 'Email already registered.'})
        return JsonResponse({'valid': True})

    if field == 'phone_number':
        if not value.isdigit() or len(value) != 10:
            return JsonResponse({'valid': False, 'message': 'Phone number must be 10 digits.'})
        if User.objects.filter(phone_number=value).exists():
            return JsonResponse({'valid': False, 'message': 'Phone number already in use.'})
        return JsonResponse({'valid': True})

    return JsonResponse({'valid': False, 'message': 'Invalid field'})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product


from django.contrib.auth.decorators import login_required, user_passes_test

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category
from django.contrib import messages

@login_required
def add_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')  # Get the category ID for editing (if exists)
        
        # If category_id is present, we're editing an existing category
        if category_id:
            category = Category.objects.get(id=category_id)
            category.name = request.POST.get('name')
            category.description = request.POST.get('description')
            category.save()
            messages.success(request, "Category updated successfully!")
        else:
            # Add a new category
            name = request.POST.get('name')
            description = request.POST.get('description')
            Category.objects.create(name=name, description=description)
            messages.success(request, "Category added successfully!")
    
    categories = Category.objects.all()
    return render(request, 'admin/add_category.html', {'categories': categories})

@login_required
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, "Category deleted successfully!")
    except Category.DoesNotExist:
        messages.error(request, "Category not found!")
    
    return redirect('add_category')



from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Import CustomUser

@login_required
def admin_users(request):
    # Exclude users who are admin (is_staff or is_superuser)
    users = CustomUser.objects.exclude(is_staff=True).exclude(is_superuser=True)
    return render(request, 'admin/admin_users.html', {'users': users})

# Delete User
@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('admin_users')



# Update to views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def add_product(request, product_id=None):
    categories = Category.objects.all()

    if request.method == 'POST':
        # Check if we're editing from the modal form
        if 'product_id' in request.POST and request.POST.get('product_id'):
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.name = request.POST.get('name')
            product.category_id = request.POST.get('category')
            product.price = request.POST.get('price')
            product.description = request.POST.get('description')
            product.quantity = request.POST.get('quantity') or 0

            # Handling the image upload (if provided)
            if 'image' in request.FILES and request.FILES['image']:
                product.image = request.FILES['image']

            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect('add_product')

        # Handle new product creation
        else:
            name = request.POST.get('name')
            category_id = request.POST.get('category')
            price = request.POST.get('price')
            description = request.POST.get('description', '')
            quantity = request.POST.get('quantity') or 0
            image = request.FILES.get('image')

            category = get_object_or_404(Category, id=category_id)

            product = Product(
                name=name,
                category=category,
                price=price,
                description=description,
                quantity=quantity,
                image=image
            )
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('add_product')

    else:
        product = None
        if product_id:
            product = get_object_or_404(Product, id=product_id)

        products = Product.objects.all()
        return render(request, 'admin/add_product.html', {
            'categories': categories,
            'products': products,
            'product': product,
        })


@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        # Fetch the product by its ID and delete it
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully!")
    else:
        messages.error(request, "Invalid request.")
    
    # Redirect back to the product listing page
    return redirect('add_product')
def admin_help(request):
    return render(request, 'admin/admin_help.html')






from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Wishlist, Purchase, Cart, CartItem, Category
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db.models import Avg, Count
from django.shortcuts import render
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Wishlist, SearchHistory

from django.db.models import Avg, Count, Q
from .models import Product, Category, Wishlist, CartItem, SearchHistory

def view_products(request):
    # Get base query for products with ratings
    base_query = Product.objects.all().annotate(
        avg_rating=Avg('ratings__rating'),
        review_count=Count('ratings')
    )
    
    # Initialize search query
    search_query = request.GET.get('search', '')
    
    # Process search if provided
    if search_query:
        # Save search to history
        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                search_query=search_query
            )
        else:
            # For anonymous users, use session key
            if not request.session.session_key:
                request.session.create()
            SearchHistory.objects.create(
                session_key=request.session.session_key,
                search_query=search_query
            )
        
        # Filter products by search query
        products = base_query.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    else:
        # If no search, show all products
        products = base_query
    
    # Get recommended products based on search history
    recommended_products = get_recommended_products(request)
    
    # Get categories and wishlist
    categories = Category.objects.all()
    wishlist = []
    if request.user.is_authenticated:
        wishlist = [w.product for w in Wishlist.objects.filter(user=request.user)]

    # ✅ Add cart count logic
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(item.quantity for item in cart_items)
    request.session['cart_count'] = cart_count

    return render(request, 'view_products.html', {
        'products': products,
        'categories': categories,
        'wishlist': wishlist,
        'recommended_products': recommended_products,
        'search_query': search_query,
        'cart_count': cart_count,  # Pass to template if needed
    })


def get_recommended_products(request):
    """
    Get recommended products based on user's search history
    """
    # Get user's search history
    if request.user.is_authenticated:
        search_history = SearchHistory.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        search_history = SearchHistory.objects.filter(session_key=request.session.session_key)
    
    # If no search history, return empty list
    if not search_history.exists():
        return []
    
    # Get last 5 searches
    recent_searches = search_history.order_by('-timestamp')[:5]
    
    # Create Q objects for each search term
    q_objects = Q()
    for search in recent_searches:
        q_objects |= Q(name__icontains=search.search_query)
        q_objects |= Q(category__name__icontains=search.search_query)
    
    # Get products matching search terms, excluding currently viewed product
    recommended = Product.objects.filter(q_objects).annotate(
        avg_rating=Avg('ratings__rating'),
        review_count=Count('ratings')
    ).distinct()
    
    # Limit to 10 products
    return recommended[:10]
    

# Utility function to get or create a cart
def get_user_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, CartItem

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request)
    
    # Check if product has enough quantity
    if product.quantity <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('view_products')
        
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Add success message
    messages.success(request, f"✅ {product.name} has been added to your cart.")
    
    return redirect('view_products')


def view_cart(request):
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate total price and item count
    total_price = 0
    cart_count = 0
    for item in cart_items:
        item.subtotal = item.quantity * item.product.price
        total_price += item.subtotal
        cart_count += item.quantity  # Count total items, not just unique products
    
    # Store cart count in session for use across the site
    request.session['cart_count'] = cart_count
    
    return render(request, 'cart.html', {
        'items': cart_items, 
        'total_price': total_price,
        'cart_count': cart_count
    })


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = get_user_cart(request)
        for item in CartItem.objects.filter(cart=cart):
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity and quantity.isdigit():
                item.quantity = max(1, int(quantity))  # Ensure at least 1
                item.save()
        
        # ✅ Add success message
        messages.success(request, "✅ Your cart has been updated successfully.")
    
    return redirect('view_cart')


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import CartItem,Address

@login_required
def remove_from_cart(request, item_id):
    cart = get_user_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()

    # ✅ Add success message
    messages.success(request, "🛒 Item removed from your cart.")

    return redirect('view_cart')
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Product, Wishlist

@require_POST
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        wishlist_item.delete()
        status = "removed"
        message = "💔 Removed from wishlist"
    else:
        status = "added"
        message = "💖 Added to wishlist"
    
    # Include message in JSON (to show via JS)
    return JsonResponse({"status": status, "message": message})

   

from django.contrib.auth.decorators import login_required
from .models import Wishlist, CartItem

@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    
    # ✅ Add cart count logic
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(item.quantity for item in cart_items)
    request.session['cart_count'] = cart_count

    return render(request, 'wishlist.html', {
        'wishlist': wishlist,
        'cart_count': cart_count,  # Optional: pass to template if needed
    })


# New view for the buy page (replaces the modal)
@login_required
def buy_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock
    if product.quantity <= 0:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "This product is out of stock")
        return redirect('view_products')
    
    return render(request, 'buy_page.html', {'product': product})


@login_required
@require_POST
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock
    if product.quantity <= 0:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "This product is out of stock")
        return redirect('view_products')
    
    # Process purchase if POST data is valid
    address = request.POST.get('address')
    payment_mode = request.POST.get('payment_mode')
    
    if address and payment_mode:
        # Create purchase record
        purchase = Purchase.objects.create(
            user=request.user,
            product=product,
            date_bought=timezone.now(),
            delivery_address=address,
            payment_mode=payment_mode
        )
        
        # Update product quantity
        product.quantity -= 1
        product.save()
        
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.success(request, f"Successfully purchased {product.name}!")
        
        return redirect('bought_items')
    
    return redirect('view_products')



# Add these views to your views.py file

@login_required
def manage_addresses(request):
    """View to manage user addresses"""
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Handle form submission for new address
        name = request.POST.get('name')
        phone = request.POST.get('phone') 
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        is_default = request.POST.get('is_default') == 'on'
        
        if name and phone and address_line and city and state and pincode:
            # Create new address
            Address.objects.create(
                user=request.user,
                name=name,
                phone_number=phone,
                address_line=address_line,
                city=city,
                state=state,
                pincode=pincode,
                is_default=is_default
            )
            
            if hasattr(request, 'messages'):
                from django.contrib import messages
                messages.success(request, "Address added successfully")
            
            # Redirect to addresses page or checkout
            next_url = request.POST.get('next', 'manage_addresses')
            return redirect(next_url)
        else:
            if hasattr(request, 'messages'):
                from django.contrib import messages
                messages.error(request, "Please fill all required fields")
    
    return render(request, 'manage_addresses.html', {
        'addresses': addresses
    })

@login_required
def delete_address(request, address_id):
    """Delete a user address"""
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        was_default = address.is_default
        address.delete()
        
        # If we deleted a default address, set a new default if any addresses remain
        if was_default:
            remaining = Address.objects.filter(user=request.user).first()
            if remaining:
                remaining.is_default = True
                remaining.save()
        
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.success(request, "Address deleted successfully")
    except Address.DoesNotExist:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "Address not found")
    
    # Get the next URL or default to addresses page
    next_url = request.GET.get('next', 'manage_addresses')
    return redirect(next_url)

@login_required
def set_default_address(request, address_id):
    """Set an address as default"""
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        
        # Set all addresses as not default
        Address.objects.filter(user=request.user).update(is_default=False)
        
        # Set the selected address as default
        address.is_default = True
        address.save()
        
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.success(request, "Default address updated")
    except Address.DoesNotExist:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "Address not found")
    
    # Get the next URL or default to addresses page
    next_url = request.GET.get('next', 'manage_addresses')
    return redirect(next_url)

# Update your existing checkout view to include addresses
@login_required
def checkout(request):
    """View for displaying the checkout page with all cart items"""
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Check if cart is empty
    if not cart_items:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "Your cart is empty")
        return redirect('view_cart')
    
    # Get user addresses
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first()
    
    # Calculate total price
    total_price = 0
    for item in cart_items:
        item.subtotal = item.quantity * item.product.price
        total_price += item.subtotal
    
    return render(request, 'checkout.html', {
        'items': cart_items,
        'total_price': total_price,
        'addresses': addresses,
        'default_address': default_address
    })

# Update your process_checkout view to use selected address
@login_required
@require_POST
def process_checkout(request):
    """Process the checkout for all items in the cart"""
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Check if cart is empty
    if not cart_items:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "Your cart is empty")
        return redirect('view_cart')
    
    # Get address and payment mode
    address_id = request.POST.get('address_id')
    payment_mode = request.POST.get('payment_mode')
    
    try:
        if address_id:
            # Get selected address
            delivery_address = Address.objects.get(id=address_id, user=request.user)
            address_text = f"{delivery_address.name}, {delivery_address.phone_number}, {delivery_address.address_line}, {delivery_address.city}, {delivery_address.state} - {delivery_address.pincode}"
        else:
            # Fallback to form-entered address
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            
            if all([name, phone, address, city, state, pincode]):
                address_text = f"{name}, {phone}, {address}, {city}, {state} - {pincode}"
            else:
                raise ValueError("Missing address information")
        
        if payment_mode and address_text:
            # Flag to check if any product is out of stock
            stock_issue = False
            
            # Create purchase records for each item
            for item in cart_items:
                product = item.product
                
                # Check if product has enough quantity
                if product.quantity < item.quantity:
                    if hasattr(request, 'messages'):
                        from django.contrib import messages
                        messages.error(request, f"Not enough stock for {product.name}. Only {product.quantity} available.")
                    stock_issue = True
                    continue
                
                # Create purchase record
                purchase = Purchase.objects.create(
                    user=request.user,
                    product=product,
                    quantity=item.quantity,
                    date_bought=timezone.now(),
                    delivery_address=address_text,
                    payment_mode=payment_mode
                )
                
                # Update product quantity
                product.quantity -= item.quantity
                product.save()
                
                # Remove from cart after successful purchase
                item.delete()
            
            if stock_issue:
                return redirect('view_cart')
            
            if hasattr(request, 'messages'):
                from django.contrib import messages
                messages.success(request, "Your order has been placed successfully!")
            
            return redirect('bought_items')
    
    except (Address.DoesNotExist, ValueError) as e:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "Please select or provide a valid delivery address")
    
    return redirect('checkout')




@login_required
def buy_now_checkout(request, product_id):
    """
    Creates a temporary cart with only the selected product for checkout
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock
    if product.quantity <= 0:
        if hasattr(request, 'messages'):
            from django.contrib import messages
            messages.error(request, "This product is out of stock")
        return redirect('view_products')
    
    # Clear any existing cart
    cart = get_user_cart(request)
    CartItem.objects.filter(cart=cart).delete()
    
    # Add this product to cart with quantity 1
    CartItem.objects.create(cart=cart, product=product, quantity=1)
    
    # Redirect to checkout
    return redirect('checkout')









from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Product, Purchase, Wishlist, Cart, CartItem, Category
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
import json

# Your existing views here (view_products, add_to_cart, etc.)

# Add these new views for purchased items and admin orders

@login_required
def bought_items(request):
    """View for displaying purchased items for the currently logged-in user"""
    purchases = Purchase.objects.filter(user=request.user).order_by('-date_bought')
    
    # You may want to add pagination for better performance with many purchases
    paginator = Paginator(purchases, 9)  # Show 9 purchases per page
    page = request.GET.get('page')
    purchases = paginator.get_page(page)
    
    return render(request, 'bought_items.html', {'purchases': purchases})


# Admin views - make sure to protect them with appropriate permissions
def is_admin(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_admin)
def admin_orders(request):
    """Admin view for managing all orders"""
    # Apply filters if provided
    filter_status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Start with all purchases
    orders = Purchase.objects.all().order_by('-date_bought')
    
    # Apply status filter
    if filter_status:
        orders = orders.filter(status=filter_status)
    
    # Apply date range filters
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            orders = orders.filter(date_bought__gte=date_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            # Add one day to include the end date fully
            date_to = date_to + timedelta(days=1)
            orders = orders.filter(date_bought__lt=date_to)
        except ValueError:
            pass
    
    # Calculate stats for dashboard
    total_orders = Purchase.objects.count()
    pending_orders = Purchase.objects.filter(status='processing').count()
    delivered_orders = Purchase.objects.filter(status='delivered').count()
    
    # Calculate total revenue (assuming quantity field exists, or default to 1)
    total_revenue = Purchase.objects.aggregate(
        total=Sum(F('product__price') * F('quantity'))
    )['total'] or 0
    
    # If quantity field doesn't exist in your model, use this instead:
    # total_revenue = Purchase.objects.aggregate(total=Sum('product__price'))['total'] or 0
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'total_revenue': round(total_revenue, 2),
    }
    
    return render(request, 'admin/admin_orders.html', context)


@user_passes_test(is_admin)
def admin_order_details(request):
    """AJAX view to get order details"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order_id = request.GET.get('order_id')
        if order_id:
            try:
                order = Purchase.objects.get(id=order_id)
                html = render_to_string('admin_order_detail_partial.html', {'order': order})
                return HttpResponse(html)
            except Purchase.DoesNotExist:
                return HttpResponse('<div class="alert alert-danger">Order not found.</div>')
    
    return HttpResponse('<div class="alert alert-danger">Invalid request.</div>')


@user_passes_test(is_admin)
def admin_update_order_status(request):
    """View to update order status"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if order_id and new_status:
            try:
                order = Purchase.objects.get(id=order_id)
                order.status = new_status
                order.admin_notes = notes
                order.last_updated = timezone.now()
                order.save()
                
                # Add success message
                from django.contrib import messages
                messages.success(request, f"Order #{order_id} status updated to {new_status}")
                
                return redirect('admin_orders')
            except Purchase.DoesNotExist:
                from django.contrib import messages
                messages.error(request, "Order not found")
        else:
            from django.contrib import messages
            messages.error(request, "Invalid request parameters")
    
    return redirect('admin_orders')


@user_passes_test(is_admin)
def admin_export_orders(request):
    """Export orders as CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 'Email', 'Product', 'Quantity', 'Price', 
                    'Date', 'Status', 'Payment Method', 'Delivery Address'])
    
    # Apply filters if provided
    filter_status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Start with all purchases
    orders = Purchase.objects.all().order_by('-date_bought')
    
    # Apply filters (same as in admin_orders view)
    if filter_status:
        orders = orders.filter(status=filter_status)
    
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            orders = orders.filter(date_bought__gte=date_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            date_to = date_to + timedelta(days=1)
            orders = orders.filter(date_bought__lt=date_to)
        except ValueError:
            pass
    
    for order in orders:
        writer.writerow([
            order.id,
            order.user.get_full_name() or order.user.username,
            order.user.email,
            order.product.name,
            order.quantity if hasattr(order, 'quantity') else 1,
            order.product.price,
            order.date_bought.strftime('%Y-%m-%d %H:%M:%S'),
            order.status,
            order.payment_mode,
            order.delivery_address
        ])
    
    return response







from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductRating, Purchase
from django.contrib.auth.decorators import login_required

@login_required
def submit_rating(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        review_text = request.POST.get('review', '').strip()

        # Ensure user has purchased the product
        if not Purchase.objects.filter(user=request.user, product=product).exists():
            messages.error(request, "You can only rate products you have purchased.")
            return redirect('bought_items')

        # Avoid duplicate rating
        if ProductRating.objects.filter(product=product, user=request.user).exists():
            messages.warning(request, "You already rated this product.")
            return redirect('bought_items')

        # Create the rating and review
        ProductRating.objects.create(
            product=product,
            user=request.user,
            rating=rating_value,
            review=review_text
        )

        messages.success(request, "Thank you for rating this product!")

    return redirect('bought_items')

