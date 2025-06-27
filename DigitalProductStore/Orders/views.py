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
def confirmed_orders(request):
    customer = request.user.customer_profile
    orders = Order.objects.filter(owner=customer, order_status=Order.ORDER_CONFIRMED, delete_status=Order.LIVE)
    return render(request, 'confirmed_orders.html', {'orders': orders})

@require_POST
@login_required
def confirm_order(request):
    customer = request.user.customer_profile
    try:
        # Get the active cart order
        order = Order.objects.get(owner=customer, order_status=Order.CART_STAGE, delete_status=Order.LIVE)

        # Confirm the order
        order.order_status = Order.ORDER_CONFIRMED
        order.save()

        # Prepare download links
        product_links = []
        for item in order.ordered_items.select_related('product'):
            if item.product and item.product.url:
                product_links.append(
                    f"<li><strong>{item.product.title}:</strong> <a href='{item.product.url}'>{item.product.url}</a></li>"
                )

                # Compose email HTML content
                html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{
            font-family: 'Segoe UI', sans-serif;
            background-color: #f7f9fc;
            padding: 40px 20px;
            color: #333;
            }}
            .container {{
            max-width: 700px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            }}
            .header {{
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
            }}
            .header h1 {{
            color: #2c3e50;
            }}
            .product {{
            margin-top: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background-color: #f9f9f9;
            }}
            .product h3 {{
            margin: 0 0 10px 0;
            color: #007bff;
            }}
            .footer {{
            margin-top: 40px;
            font-size: 14px;
            color: #555;
            border-top: 1px solid #eee;
            padding-top: 20px;
            text-align: center;
            }}
            a {{
            color: #1a73e8;
            }}
        </style>
        </head>
        <body>
        <div class="container">
            <div class="header">
            <h1>🎉 Thanks for your Purchase!</h1>
            <p>Your digital products are ready for download below.</p>
            </div>
        """

        # Add product blocks
        for item in order.ordered_items.select_related('product'):
            product = item.product
            if product:
                html_content += f"""
                <div class="product">
                <h3>{product.title}</h3>
                <p><strong>Price:</strong> ₹{product.price}</p>
                <p><strong>Description:</strong> {product.description}</p>
                <p><strong>Category:</strong> {product.category}</p>
                <p><strong>Quantity Ordered:</strong> {item.quantity}</p>
                <p><strong>Download Link:</strong> <a href="{product.url}">{product.url}</a></p>
                </div>
                """

        # Close HTML
        html_content += """
            <div class="footer">
            <p>If you have any questions, reply to this email or contact support.</p>
            <p>💼 DigitalProductStore<br>📧 midhunnk2019@gmail.com</p>
            </div>
        </div>
        </body>
        </html>
        """



               # Send the email
        message = Mail(
            from_email=config('DEFAULT_FROM_EMAIL'),
            to_emails=request.user.email,
            subject='Your Digital Product Download Links',
            html_content=html_content
        )

        SENDGRID_API_KEY = config('SENDGRID_API_KEY')
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("SendGrid response status:", response.status_code)


    except Order.DoesNotExist:
        pass
    except Exception as e:
        print("SendGrid error:", e)

    return redirect('confirmed_orders')