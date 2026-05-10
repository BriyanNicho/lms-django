from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nama Kelas")
    description = models.TextField(verbose_name="Deskripsi Kelas")
    
    # RELASI SUPER: Hanya user dengan role 'TEACHER' yang bisa dipilih jadi pengajar!
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'TEACHER'},
        related_name='courses_taught',
        verbose_name="Pengajar"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Material(models.Model):
    class MaterialType(models.TextChoices):
        PDF = "PDF", "PDF Document"
        VIDEO = "VIDEO", "Video"
        PPT = "PPT", "PowerPoint"
        LINK = "LINK", "External Link"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200, verbose_name="Judul Materi")
    material_type = models.CharField(max_length=10, choices=MaterialType.choices, verbose_name="Tipe Materi")
    
    content_url = models.URLField(blank=True, null=True, verbose_name="Link Eksternal")
    # File akan otomatis masuk ke folder media/materials/ di dalam projectmu
    file = models.FileField(upload_to='materials/', blank=True, null=True, verbose_name="File Materi")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"