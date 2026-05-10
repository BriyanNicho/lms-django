from django.contrib import admin
from .models import Assignment, Submission, Quiz, Question

# Trik agar Dosen bisa langsung melihat soal di dalam halaman Kuis
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Quiz, QuizAdmin)