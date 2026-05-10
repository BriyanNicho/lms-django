from django.db import models
from django.conf import settings
from courses.models import Course # Mengambil data kelas

class AttendanceSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_sessions', verbose_name="Kelas")
    session_date = models.DateField(verbose_name="Tanggal Sesi")
    start_time = models.TimeField(verbose_name="Jam Mulai")
    end_time = models.TimeField(verbose_name="Jam Selesai")
    is_active = models.BooleanField(default=True, verbose_name="Sesi Aktif")

    def __str__(self):
        return f"Sesi {self.course.title} - {self.session_date}"

class AttendanceRecord(models.Model):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    # Relasi: Hanya user STUDENT yang bisa presensi
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'STUDENT'},
        verbose_name="Mahasiswa"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Presensi")
    STATUS_CHOICES = [
        ('PRESENT', 'Hadir'),
        ('LATE', 'Terlambat'),
        ('ABSENT', 'Alpa'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')

    class Meta:
        # Mencegah mahasiswa presensi dua kali di sesi yang sama
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.session}"