from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Kita mengatur agar field 'role' muncul di halaman edit user
class CustomUserAdmin(UserAdmin):
    model = User
    # Menampilkan kolom Role di tabel daftar user
    list_display = ['username', 'email', 'role', 'is_staff']
    
    # Menambahkan bagian "Peran" di halaman edit user (yang kamu buka di gambar)
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Peran', {'fields': ('role', 'phone_number')}),
    )

# Daftarkan Custom User kita
admin.site.register(User, CustomUserAdmin)