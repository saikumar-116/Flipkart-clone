from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Cart
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),

    # Checkout & Payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('order-success/', views.order_success, name='order_success'),

    # Product Details ✅ ADDED
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # Life Events
    path('life-events/', views.life_events, name='life_events'),
    path('life-events/<int:event_id>/', views.event_products, name='event_products'),

    # Group Buying
    path('group-deals/', views.group_deals, name='group_deals'),
    path('join-group/<int:deal_id>/', views.join_group_deal, name='join_group_deal'),

    path('my-orders/', views.my_orders, name='my_orders'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Cancel Order
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),


]
