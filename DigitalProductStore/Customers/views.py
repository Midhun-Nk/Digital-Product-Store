from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomerModels
from .models import SellerModels  # ✅ Import your seller model


def user_logout(request):
    logout(request)
    return redirect('Home')


def show_account(request):
    error = ""

    if request.method == "POST":
        try:
            # ✅ Registration Logic
            if 'register' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )

                CustomerModels.objects.create(
                    user=user,
                    name=username,
                    phone=phone,
                    address=address
                )
                return redirect('Home')

            # ✅ Login Logic
            elif 'login' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('Home')
                else:
                    error = "Invalid username or password."

        except IntegrityError:
            error = "Username or email already exists."
        except Exception as e:
            error = str(e)

    return render(request, 'acount.html', {"error": error})


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
