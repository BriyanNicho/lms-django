from django.db import models
from django.conf import settings
from courses.models import Course # Mengambil data kelas

class Thread(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='threads', verbose_name="Kelas")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Pembuat Topik")
    title = models.CharField(max_length=200, verbose_name="Judul Topik")
    content = models.TextField(verbose_name="Isi Diskusi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='replies', verbose_name="Topik Diskusi")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Penulis")
    content = models.TextField(verbose_name="Isi Balasan")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Balasan dari {self.author.username} di '{self.thread.title}'"