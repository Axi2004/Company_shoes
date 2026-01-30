from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

            # Проверяем поле role вместо групп
            if user.role == 'admin':
                return redirect('admin')
            elif user.role == 'manager':
                return redirect('manager')
            else:  # client
                return redirect('client')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def client(request):
    return render(request, 'client.html')
def admin(request):
    return render(request, 'admin.html')

def manager(request):
    return render(request, 'manager.html')