from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Definisi pilihan Role
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Pengajar"
        STUDENT = "STUDENT", "Mahasiswa"

    # Field role dengan default sebagai Mahasiswa
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.STUDENT
    )
    
    # Tambahan field opsional
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"