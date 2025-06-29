from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomerModels
from Seller.models import SellerModels  # ✅ Import your seller model
from Products.models import ProductModels


def user_logout(request):
    logout(request)
    return redirect('home')


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
                return redirect('home')

            # ✅ Login Logic
            elif 'login' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    error = "Invalid username or password."

        except IntegrityError:
            error = "Username or email already exists."
        except Exception as e:
            error = str(e)

    return render(request, 'acount.html', {"error": error})

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')
