from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Material
from assessments.models import Assignment, Quiz
from attendance.models import AttendanceSession
from forums.models import Thread

@login_required
def course_detail(request, course_id):
    """Tampilkan detail kelas dengan materials, tugas, kuis, dan presensi"""
    course = get_object_or_404(Course, id=course_id)
    
    context = {
        'course': course,
        'materials': course.materials.all(),
        'assignments': course.assignments.all(),
        'quizzes': course.quizzes.all(),
        'attendance_sessions': course.attendance_sessions.all(),
        'threads': course.threads.all(),
    }
    
    return render(request, 'courses/course_detail.html', context)

@login_required
def course_materials(request, course_id):
    """Tampilkan semua materi dalam satu kelas"""
    course = get_object_or_404(Course, id=course_id)
    materials = course.materials.all()
    
    context = {
        'course': course,
        'materials': materials,
    }
    
    return render(request, 'courses/course_materials.html', context)
