#Hospital management django

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('blog/', views.blog, name='blog'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),




    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
   
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    path('products/add/', views.add_product, name='add_product'),
    
     path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

     path('help/', views.admin_help, name='admin_help'),
      path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('products/', views.view_products, name='view_products'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('purchased/', views.bought_items, name='bought_items'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('purchases/', views.bought_items, name='bought_items'),
    path('buy-page/<int:product_id>/', views.buy_page, name='buy_page'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_checkout, name='process_checkout'),
    path('buy-now-checkout/<int:product_id>/', views.buy_now_checkout, name='buy_now_checkout'),
    
    
    
    # Admin URLs - make sure to protect these with proper permission checks
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/details/', views.admin_order_details, name='admin_order_details'),
    path('orders/update-status/', views.admin_update_order_status, name='admin_update_order_status'),
    path('orders/export/', views.admin_export_orders, name='admin_export_orders'),
    
    
    path('rate-product/<int:product_id>/', views.submit_rating, name='submit_rating'),
    path('validate/', views.validate_field, name='validate_field'),
    path('manage-addresses/', views.manage_addresses, name='manage_addresses'),
    path('set_default_address/<int:address_id>/', views.set_default_address, name='set_default_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address')
    
]
