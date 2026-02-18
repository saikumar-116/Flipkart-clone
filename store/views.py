from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Wishlist


from .models import (
    Product,
    Order,
    OrderItem,
    LifeEvent,
    EventProduct,
    GroupDeal,
    GroupDealMember,
    Review
)

# ================= HOME =================
def home(request):
    q = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=q)) if q else Product.objects.all()

    events = LifeEvent.objects.all()                  # ✅ Shop by Life Events
    group_deals = GroupDeal.objects.filter(active=True)  # ✅ Group Buying on Home

    return render(request, 'home.html', {
        'products': products,
        'events': events,
        'group_deals': group_deals                    # ✅ SEND TO TEMPLATE
    })


# ================= PRODUCT DETAILS =================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)

    if request.method == "POST" and request.user.is_authenticated:
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

        return redirect('product_detail', id=product.id)

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews
    })


# ================= AUTH =================
def signup_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("emailpassword")

        if not username or not email or not password:
            error = "All fields are required"

        elif User.objects.filter(username=username).exists():
            error = "Username already exists"

        elif User.objects.filter(email=email).exists():
            error = "Email already registered"

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('home')

    return render(request, 'signup.html', {'error': error})


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


# ================= CART =================
def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    pid = str(id)
    cart[pid] = cart.get(pid, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    pid = str(id)

    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]

    request.session['cart'] = cart
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=pid)
        product.quantity = qty
        product.subtotal = product.price * qty
        total += product.subtotal
        products.append(product)

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })
    # ================= WISHLIST =================
@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()
    return redirect('wishlist')


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {
        'items': items
    })



# ================= CHECKOUT =================
def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=pid)
        product.quantity = qty
        product.subtotal = product.price * qty
        total += product.subtotal
        products.append(product)

    return render(request, 'checkout.html', {
        'products': products,
        'total': total
    })


# ================= PAYMENT + EMI =================
def payment(request):
    cart = request.session.get('cart', {})
    total = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=pid)
        total += product.price * qty

    emi_amount = None
    months = None
    total_emi_payment = None

    if request.method == "POST":

        if 'emi_months' in request.POST:
            months = int(request.POST.get('emi_months'))
            emi_amount = round(total / months, 2)
            total_emi_payment = total

        elif 'pay_full' in request.POST:
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                total_amount=total,
                status='PLACED'
            )

            for pid, qty in cart.items():
                product = get_object_or_404(Product, id=pid)
                OrderItem.objects.create(
                    order=order,
                    product_name=product.name,
                    price=product.price,
                    quantity=qty
                )

            request.session['cart'] = {}
            return redirect('order_success')

    return render(request, 'payment.html', {
        'total': total,
        'emi_amount': emi_amount,
        'months': months,
        'total_emi_payment': total_emi_payment
    })


def order_success(request):
    return render(request, 'order_success.html')


# ================= MY ORDERS =================
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'PLACED':
        order.status = 'CANCELLED'
        order.save()

    return redirect('my_orders')



# ================= LIFE EVENTS =================
def life_events(request):
    events = LifeEvent.objects.all()
    return render(request, 'life_events.html', {'events': events})


def event_products(request, event_id):
    event = get_object_or_404(LifeEvent, id=event_id)
    products = EventProduct.objects.filter(event=event)
    return render(request, 'event_products.html', {
        'event': event,
        'products': products
    })


# ================= GROUP BUYING =================
@login_required
def group_deals(request):
    deals = GroupDeal.objects.filter(active=True)
    return render(request, 'group_deals.html', {'deals': deals})


@login_required
def join_group_deal(request, deal_id):
    deal = get_object_or_404(GroupDeal, id=deal_id)
    GroupDealMember.objects.get_or_create(
        group_deal=deal,
        user=request.user
    )
    return redirect('group_deals')
