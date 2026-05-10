from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from courses.models import Course
from .models import Assignment, Submission, Quiz, Question
from datetime import datetime

@login_required
def assignment_list(request, course_id):
    """Tampilkan daftar tugas dalam satu kelas"""
    course = get_object_or_404(Course, id=course_id)
    assignments = course.assignments.all().order_by('-due_date')
    
    context = {
        'course': course,
        'assignments': assignments,
    }
    
    return render(request, 'assessments/assignment_list.html', context)

@login_required
def assignment_detail(request, assignment_id):
    """Tampilkan detail tugas dan form pengumpulan"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Cek apakah user sudah submit
    user_submission = Submission.objects.filter(
        assignment=assignment, 
        student=request.user
    ).first()
    
    context = {
        'assignment': assignment,
        'user_submission': user_submission,
        'is_overdue': datetime.now() > assignment.due_date.replace(tzinfo=None) if assignment.due_date else False,
    }
    
    return render(request, 'assessments/assignment_detail.html', context)

@login_required
@require_POST
def submit_assignment(request, assignment_id):
    """Terima pengumpulan tugas dari mahasiswa"""
    if request.user.role != 'STUDENT':
        return JsonResponse({'error': 'Hanya mahasiswa yang bisa submit tugas'}, status=403)
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Cek apakah file dikirim
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'File tidak ada'}, status=400)
    
    # Cek apakah sudah submit sebelumnya
    existing = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()
    
    if existing:
        # Update file yang ada (re-submission)
        existing.file = request.FILES['file']
        existing.save()
        return JsonResponse({
            'success': True,
            'message': 'Tugas berhasil diperbarui',
        })
    else:
        # Buat submission baru
        submission = Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=request.FILES['file']
        )
        return JsonResponse({
            'success': True,
            'message': 'Tugas berhasil dikumpulkan',
            'submitted_at': submission.submitted_at.strftime('%d/%m/%Y %H:%M')
        })

@login_required
def quiz_list(request, course_id):
    """Tampilkan daftar kuis dalam satu kelas"""
    course = get_object_or_404(Course, id=course_id)
    quizzes = course.quizzes.all().order_by('-due_date')
    
    context = {
        'course': course,
        'quizzes': quizzes,
    }
    
    return render(request, 'assessments/quiz_list.html', context)

@login_required
def quiz_detail(request, quiz_id):
    """Tampilkan detail kuis dengan soal"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'question_count': questions.count(),
    }
    
    return render(request, 'assessments/quiz_detail.html', context)
