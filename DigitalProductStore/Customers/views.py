from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import CustomerModels
from django.contrib.auth import authenticate, login,logout
def user_logout(request):
    logout(request)
    return redirect('Home')  # or any other URL name you want to redirect after logout

def show_account(request):
    error = ""

    if request.method == "POST":
        try:
            # REGISTER logic
            if 'register' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')

                # Create user account
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )

                # Create customer profile (NO password here)
                CustomerModels.objects.create(
                    user=user,
                    name=username,
                    phone=phone,
                    address=address
                )
                return redirect('Home')

            # LOGIN logic
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
