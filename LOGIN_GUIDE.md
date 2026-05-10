# 📱 Panduan Login Portal Belajar LMS

## 🎯 Akses Login Page

### URL Login

```
http://localhost:8001/login/
```

---

## 🔐 Cara Login

### 1️⃣ Buka Halaman Login

- Akses `http://localhost:8001/` atau `http://localhost:8001/login/`
- Jika belum login, akan otomatis redirect ke halaman login

### 2️⃣ Masukkan Credentials

- **Username**: Masukkan username akun Anda
- **Password**: Masukkan password akun Anda
- Klik tombol **"Login"**

### 3️⃣ Fitur Login Page

✅ **Show/Hide Password** - Klik ikon mata untuk menampilkan/menyembunyikan password  
✅ **Remember Me** - Centang untuk diingat di komputer ini (opsional)  
✅ **Forgot Password** - Link untuk reset password  
✅ **Register** - Link untuk membuat akun baru

### 4️⃣ Setelah Login Berhasil

- Otomatis redirect ke **Dashboard** sesuai role
- Tampilkan welcome message
- Session dimulai

---

## 📋 Akun Demo untuk Testing

| Tipe          | Username   | Password      |
| ------------- | ---------- | ------------- |
| **Mahasiswa** | `student1` | `password123` |
| **Pengajar**  | `teacher1` | `password123` |
| **Admin**     | `admin1`   | `password123` |

> 💡 **Catatan**: Akun-akun ini harus dibuat terlebih dahulu di Admin Panel sebelum bisa login.

---

## 🔄 Logout

Untuk logout:

1. Klik tombol **"Logout"** di navbar atas kanan
2. Atau gunakan URL: `http://localhost:8001/logout/`
3. Session akan dihapus dan redirect ke halaman login

---

## 📝 Daftar Akun Baru

### Akses Register Page

```
http://localhost:8001/register/
```

### Cara Mendaftar

1. Klik link **"Daftar di sini"** di halaman login
2. Atau akses langsung `/register/`

### Form Registrasi

- **Username** - Minimal 3 karakter, tanpa spasi
- **Email** - Opsional (bisa kosong)
- **Password** - Minimal 6 karakter
- **Konfirmasi Password** - Harus sama dengan password

### Fitur Register

✅ **Real-time Password Validation** - Cek langsung apakah password cocok  
✅ **Show/Hide Password** - Toggle untuk lihat/sembunyikan  
✅ **Password Requirements** - Informasi persyaratan password  
✅ **Error Messages** - Pesan error jelas saat ada masalah

### Setelah Berhasil Daftar

- Akun akan dibuat dengan role **STUDENT** (Mahasiswa)
- Redirect ke login page
- Login dengan akun yang baru dibuat

---

## 🎨 UI Features

### Design

- 🎨 Gradient background modern
- 🎯 Centered card layout
- 📱 Mobile responsive
- 🌙 Dark theme friendly
- ✨ Smooth animations

### Components

- Input validation real-time
- Show/hide password toggle
- Remember me checkbox
- Auto-dismiss alert messages (5 detik)
- Demo credentials hint
- Bootstrap Icons integration

### Color Scheme

- **Primary Gradient**: Purple to Violet (#667eea → #764ba2)
- **Accent**: Blue buttons
- **Text**: Dark gray for readability
- **Background**: White card on gradient

---

## 🔒 Security Features

✅ **CSRF Protection** - Form CSRF token included  
✅ **Password Hashing** - Password di-hash dengan Django  
✅ **Session Management** - Secure session cookies  
✅ **Login Required** - Protected views redirect to login  
✅ **Auth Backend** - Django default authentication

---

## ⚡ Quick Commands

### View All Users (via Admin)

```
http://localhost:8001/admin/accounts/user/
```

### Create New User (via Admin)

```
http://localhost:8001/admin/accounts/user/add/
```

### Reset Password (via Admin)

```
http://localhost:8001/admin/password_change/
```

---

## 🐛 Troubleshooting

### ❌ "Username atau password salah!"

- Pastikan username & password benar
- Cek apakah akun sudah dibuat di admin
- Pastikan user aktif (is_active = True)

### ❌ Halaman login tidak muncul (error 500)

- Restart container: `docker-compose restart web`
- Cek logs: `docker-compose logs web`
- Pastikan template file ada di `templates/accounts/login.html`

### ❌ Redirect error setelah login

- Cek settings.py sudah ada `LOGIN_REDIRECT_URL`
- Pastikan dashboard view tidak error
- Lihat browser console untuk detail error

### ❌ Cannot logout

- Clear browser cache & cookies
- Cek `LOGOUT_REDIRECT_URL` di settings
- Restart container jika perlu

---

## 📊 Login Flow Diagram

```
┌─────────────────┐
│  User Akses     │
│ localhost:8001  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Belum Login?    │
│ Redirect ke     │
│ /login/         │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ Display Login Form   │
│ - Username field     │
│ - Password field     │
│ - Login button       │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ User Masukkan        │
│ Username & Password  │
└────────┬─────────────┘
         │
         ▼
    ┌────────────┐
    │ Validasi   │
    │ Credentials│
    └─┬──────┬───┘
      │      │
   ✓  │      │  ✗
      ▼      ▼
   LOGIN  ERROR MSG
    ✓      ✗
      │      │
      ▼      ▼
 SET SESSION ERROR
    │       (retry)
    ▼
 REDIRECT
    │
    ▼
DASHBOARD
(sesuai role)
```

---

## 🔑 Default Credentials (Jika Sudah Dibuat)

### Admin Account

```
URL: http://localhost:8001/admin/
Username: admin
Password: [sesuai saat setup]
```

### User Login Portal

```
URL: http://localhost:8001/login/
Username: [sesuai akun]
Password: [sesuai akun]
```

---

## 📌 Important URLs

| Halaman      | URL                     |
| ------------ | ----------------------- |
| Login        | `/login/`               |
| Register     | `/register/`            |
| Logout       | `/logout/`              |
| Dashboard    | `/`                     |
| Admin Panel  | `/admin/`               |
| Manage Users | `/admin/accounts/user/` |

---

## ✅ Status

```
Login Page:       ✅ CREATED
Register Page:    ✅ CREATED
Authentication:   ✅ WORKING
Session Mgmt:     ✅ WORKING
Role-based Auth:  ✅ WORKING
UI/UX:            ✅ MODERN
```

---

**Terakhir diupdate: 9 Mei 2024**  
**Status: ✅ Production Ready**
