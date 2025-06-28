from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Orders.models import Order, OrderItem

from Customers.models import CustomerModels
from .models import SellerModels  # ✅ Import your seller model
from Products.models import ProductModels
from Orders.models import Order
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

# Create your views here.

@login_required
def seller_panel(request):
    user = request.user

    if hasattr(user, 'seller_profile'):
        return redirect('seller_dashboard')

    if request.method == 'POST':
        # Optional: Add shop name / address here
        shop_name = request.POST.get('shop_name', f"{user.username}'s Shop")
        shop_address = request.POST.get('shop_address', 'Not provided')

        SellerModels.objects.create(
            user=user,
            shop_name=shop_name,
            shop_address=shop_address
        )

        messages.success(request, "You are now a seller!")
        return redirect('seller_dashboard')

    return render(request, 'become_seller.html')


@login_required
def seller_dashboard(request):
    return render(request, 'seller_dashboard.html')


@login_required
def add_product(request):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You must become a seller first.")
        return redirect('seller_panel')

    if request.method == "POST":
        try:
            title = request.POST['title']
            price = float(request.POST['price'])
            description = request.POST['description']
            category = request.POST['category']
            priority = int(request.POST.get('priority', 0))
            image = request.FILES['image']
            url = request.POST.get('url')  # ✅ Get the URL from the form

            ProductModels.objects.create(
                title=title,
                price=price,
                description=description,
                category=category,
                priority=priority,
                image=image,
                seller=request.user.seller_profile,
                url=url
            )

            return render(request, 'add_product.html', {'success': "Product added successfully!"})
        except Exception as e:
            return render(request, 'add_product.html', {'error': str(e)})

    return render(request, 'add_product.html')



@login_required
def view_seller_products(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller_panel')

    products = ProductModels.objects.filter(
        seller=request.user.seller_profile,
        delete_status=ProductModels.LIVE  # ✅ Only show live products
    )

    return render(request, 'view_seller_products.html', {'products': products})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(ProductModels, id=product_id)

    if request.user.seller_profile != product.seller:
        return redirect('view_seller_products')

    if request.method == 'POST':
        product.delete()  # ❌ PERMANENT DELETE
    return redirect('view_seller_products')

@login_required
def track_orders(request):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You must be a seller to view this page.")
        return redirect('seller_panel')

    seller = request.user.seller_profile

    # Get all confirmed orders that include this seller's products
    orders = Order.objects.filter(
    order_status__in=[
        Order.ORDER_CONFIRMED,
        Order.ORDER_PROCESSED,
        Order.ORDER_REJECTED
    ],
    ordered_items__product__seller=seller).distinct()


    return render(request, 'track_orders.html', {'orders': orders})

@login_required
def seller_settings(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller_panel') 

    seller = request.user.seller_profile
    success = None

    if request.method == 'POST':
        seller.shop_name = request.POST.get('shop_name', seller.shop_name)
        seller.shop_address = request.POST.get('shop_address', seller.shop_address)
        seller.save()
        success = "Seller details updated successfully!"

    return render(request, 'seller_settings.html', {'seller': seller, 'success': success})



@login_required
def view_pending_orders(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller_panel')

    seller = request.user.seller_profile
    orders = Order.objects.filter(
        order_status=Order.ORDER_CONFIRMED,
        ordered_items__product__seller=seller
    ).distinct()

    return render(request, 'view_pending_orders.html', {'orders': orders})

@login_required
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, order_status=Order.ORDER_CONFIRMED)

    # Generate the same email HTML (your format retained)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8" />
    <title>Your Digital Product</title>
    <style>
        body {{
        font-family: 'Segoe UI', sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
        }}
        .container {{
        max-width: 600px;
        margin: 30px auto;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        overflow: hidden;
        }}
        .header {{
        background-color: #007bff;
        color: white;
        padding: 20px 30px;
        text-align: center;
        }}
        .header h1 {{
        margin: 0;
        font-size: 24px;
        }}
        .content {{
        padding: 30px;
        }}
        .product {{
        background: #f9f9f9;
        padding: 15px 20px;
        border-left: 5px solid #007bff;
        margin-bottom: 20px;
        border-radius: 6px;
        }}
        .product h3 {{
        margin: 0;
        color: #333;
        }}
        .product p {{
        margin: 5px 0;
        font-size: 14px;
        }}
        .footer {{
        background: #f1f1f1;
        text-align: center;
        padding: 20px;
        font-size: 13px;
        color: #777;
        }}
        a.button {{
        display: inline-block;
        background-color: #007bff;
        color: white !important;
        padding: 10px 20px;
        margin-top: 10px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        }}
        a {{
        color: #007bff;
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
        <h1>🎉 Thank You for Your Purchase!</h1>
        </div>
        <div class="content">
        <p>Hi {request.user.first_name or request.user.username},</p>
        <p>Your order has been successfully processed. Below are your digital products:</p>
    """

    # Append each product block
    for item in order.ordered_items.select_related('product'):
        product = item.product
        if product:
            html_content += f"""
            <div class="product">
            <h3>{product.title}</h3>
            <p><strong>Price:</strong> ₹{product.price}</p>
            <p><strong>Description:</strong> {product.description}</p>
            <p><strong>Category:</strong> {product.category}</p>
            <p><strong>Quantity:</strong> {item.quantity}</p>
            <a class="button" href="{product.url}">Download</a>
            </div>
            """

    # Close the email
    html_content += """
        <p>If you have any questions, feel free to reply to this email.</p>
        </div>
        <div class="footer">
        <p>💼 DigitalProductStore<br>
            📧 support@digitalproductstore.com</p>
        </div>
    </div>
    </body>
    </html>
    """

    try:
        message = Mail(
            from_email=config('DEFAULT_FROM_EMAIL'),
            to_emails=order.owner.user.email,
            subject='Your Digital Product Download Links',
            html_content=html_content
        )
        sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
        response = sg.send(message)
        print("SendGrid response status:", response.status_code)

        order.order_status = Order.ORDER_PROCESSED
        order.save()
    except Exception as e:
        print("SendGrid error:", e)

    return redirect('view_pending_orders')


@login_required
def reject_order(request, order_id):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller_panel')

    order = get_object_or_404(Order, id=order_id, order_status=Order.ORDER_CONFIRMED)

    try:
        order.order_status = Order.ORDER_REJECTED
        order.save()

        # Optional: send rejection email
        message = Mail(
            from_email=config('DEFAULT_FROM_EMAIL'),
            to_emails=order.owner.user.email,
            subject='Your Order Was Cancelled',
            html_content=f"""
            <h2>Order Cancelled</h2>
            <p>We're sorry, but your recent order #{order.id} has been cancelled by the seller.</p>
            <p>Please contact support if you believe this was a mistake.</p>
            """
        )
        sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
        sg.send(message)

        messages.warning(request, "Order was rejected and buyer notified.")

    except Exception as e:
        print("Error rejecting order:", e)
        messages.error(request, "Failed to reject the order.")

    return redirect('view_pending_orders')

