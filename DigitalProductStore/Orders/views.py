from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from Products.models import ProductModels
from Customers.models import CustomerModels
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.core.mail import send_mail
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Get or create customer profile
        customer = getattr(user, 'customer_profile', None)
        if not customer:
            customer = CustomerModels.objects.create(user=user)

        # Get product
        product = get_object_or_404(ProductModels, pk=product_id)

        # Get or create the active cart order
        order, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE,
            delete_status=Order.LIVE,
        )

        # Get or create order item
        order_item, created = OrderItem.objects.get_or_create(
            owner=order,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        return redirect('view_cart')  # cart page

    return redirect('home')  # fallback
@login_required
def view_cart(request):
    user = request.user
    customer = getattr(user, 'customer_profile', None)
    
    if not customer:
        return render(request, 'cart.html', {'items': [], 'subtotal': 0, 'tax': 0, 'total': 0})

    try:
        order = Order.objects.get(
            owner=customer,
            order_status=Order.CART_STAGE,
            delete_status=Order.LIVE
        )
        order_items = order.ordered_items.select_related('product')

        items = []
        subtotal = 0
        for item in order_items:
            if item.product:
                item_total = item.product.price * item.quantity
                subtotal += item_total
                items.append({'item': item, 'subtotal': item_total})

        tax = subtotal * 0.1  # 10% tax
        total = subtotal + tax

    except Order.DoesNotExist:
        items = []
        subtotal = 0
        tax = 0
        total = 0

    return render(request, 'cart.html', {
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    })

@require_POST
@login_required
def update_cart_quantity(request, item_id):
    action = request.POST.get('action')
    item = get_object_or_404(OrderItem, id=item_id, owner__owner__user=request.user)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return redirect('view_cart')


@require_POST
@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, owner__owner__user=request.user)
    item.delete()
    return redirect('view_cart')


@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, owner=request.user.customer_profile)

    items = []
    for item in order.ordered_items.select_related('product'):
        total = item.quantity * item.product.price if item.product else 0
        items.append({
            'item': item,
            'total': total
        })

    return render(request, 'order_status.html', {
        'order': order,
        'items': items
    })

@require_POST
@login_required

def confirm_order(request):
    user = request.user
    customer = getattr(user, 'customer_profile', None)

    if not customer:
        return redirect('view_cart')

    try:
        order = Order.objects.get(
            owner=customer,
            order_status=Order.CART_STAGE,
            delete_status=Order.LIVE
        )

        # Update order status
        order.order_status = Order.ORDER_CONFIRMED
        order.save()

    except Order.DoesNotExist:
        return redirect('view_cart')

    return redirect('confirmed_orders')

@login_required
def confirmed_orders(request):
    customer = request.user.customer_profile

    orders = Order.objects.filter(
        owner=customer,
        order_status__in=[Order.ORDER_CONFIRMED, Order.ORDER_PROCESSED, Order.ORDER_REJECTED],
        delete_status=Order.LIVE
    ).order_by('-created_at')

    return render(request, 'confirmed_orders.html', {'orders': orders})
