from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Customers.models import CustomerModels
from .models import SellerModels  # ✅ Import your seller model
from Products.models import ProductModels

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