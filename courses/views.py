from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CourseForm
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


@login_required
def course_create(request):
    if request.user.role != 'TEACHER':
        messages.error(request, 'Anda tidak memiliki akses untuk membuat kursus.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Kursus berhasil dibuat.')
            return redirect('dashboard')
    else:
        form = CourseForm()

    return render(
        request,
        'courses/course_form.html',
        {
            'form': form,
            'page_title': 'Buat Kursus Baru',
            'submit_label': 'Simpan Kursus',
        },
    )


@login_required
def course_edit(request, course_id):
    if request.user.role != 'TEACHER':
        messages.error(request, 'Anda tidak memiliki akses untuk mengedit kursus.')
        return redirect('dashboard')

    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kursus berhasil diperbarui.')
            return redirect('dashboard')
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        'courses/course_form.html',
        {
            'form': form,
            'course': course,
            'page_title': 'Edit Kursus',
            'submit_label': 'Simpan Perubahan',
        },
    )
