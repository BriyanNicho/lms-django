from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from courses.models import Course
from .models import User

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Halaman login custom"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autentikasi user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau password salah!')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Anda telah logout. Sampai jumpa!')
    return redirect('login')

@require_http_methods(["GET", "POST"])
def register_view(request):
    """Halaman register (opsional, bisa diaktifkan jika ingin self-registration)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validasi
        if not username or not password:
            messages.error(request, 'Username dan password harus diisi!')
            return redirect('register')
        
        if password != password_confirm:
            messages.error(request, 'Password tidak cocok!')
            return redirect('register')
        
        if len(password) < 6:
            messages.error(request, 'Password minimal 6 karakter!')
            return redirect('register')
        
        # Cek apakah username sudah ada
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah terdaftar!')
            return redirect('register')
        
        # Buat user baru (default role STUDENT)
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='STUDENT'  # Default role
            )
            messages.success(request, 'Pendaftaran berhasil! Silakan login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Gagal mendaftar: {str(e)}')
            return redirect('register')
    
    return render(request, 'accounts/register.html')

@login_required
def dashboard(request):
    """Dashboard utama - reroute ke dashboard sesuai role"""
    user = request.user
    context = {}

    if user.role == 'ADMIN':
        context['total_courses'] = Course.objects.count()
        return render(request, 'dashboard/admin.html', context)
    
    elif user.role == 'TEACHER':
        context['my_courses'] = Course.objects.filter(teacher=user)
        return render(request, 'dashboard/teacher.html', context)
    
    else:  # Mahasiswa (STUDENT)
        context['available_courses'] = Course.objects.all()
        return render(request, 'dashboard/student.html', context)