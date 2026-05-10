from django.db import models
from django.conf import settings
from courses.models import Course # Mengambil data Kelas dari app courses

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200, verbose_name="Judul Tugas")
    description = models.TextField(verbose_name="Deskripsi Tugas")
    due_date = models.DateTimeField(verbose_name="Batas Waktu (Deadline)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    # Relasi: Hanya user dengan role STUDENT yang bisa mengumpulkan tugas
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'STUDENT'},
        verbose_name="Mahasiswa"
    )
    # File jawaban mahasiswa akan masuk ke folder media/submissions/
    file = models.FileField(upload_to='submissions/', verbose_name="File Jawaban")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Pengumpulan")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Nilai")
    feedback = models.TextField(null=True, blank=True, verbose_name="Feedback Dosen")

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200, verbose_name="Judul Kuis")
    due_date = models.DateTimeField(verbose_name="Batas Waktu (Deadline)")

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Pertanyaan")
    option_a = models.CharField(max_length=200, verbose_name="Pilihan A")
    option_b = models.CharField(max_length=200, verbose_name="Pilihan B")
    option_c = models.CharField(max_length=200, verbose_name="Pilihan C")
    option_d = models.CharField(max_length=200, verbose_name="Pilihan D")
    
    # Kunci Jawaban
    CORRECT_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES, verbose_name="Kunci Jawaban")

    def __str__(self):
        return self.text