from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from courses.models import Course
from .models import AttendanceSession, AttendanceRecord

@login_required
def attendance_list(request, course_id):
    """Tampilkan daftar sesi presensi untuk satu kelas"""
    course = get_object_or_404(Course, id=course_id)
    sessions = course.attendance_sessions.all()
    
    context = {
        'course': course,
        'sessions': sessions,
    }
    
    return render(request, 'attendance/attendance_list.html', context)

@login_required
def attendance_session_detail(request, session_id):
    """Tampilkan detail sesi presensi dan form presensi"""
    session = get_object_or_404(AttendanceSession, id=session_id)
    
    # Cek apakah user sudah presensi
    user_attendance = AttendanceRecord.objects.filter(
        session=session, 
        student=request.user
    ).first()
    
    context = {
        'session': session,
        'user_attendance': user_attendance,
        'is_active': session.is_active,
    }
    
    return render(request, 'attendance/attendance_detail.html', context)

@login_required
@require_POST
def mark_attendance(request, session_id):
    """Catat presensi mahasiswa"""
    if request.user.role != 'STUDENT':
        return JsonResponse({'error': 'Hanya mahasiswa yang bisa presensi'}, status=403)
    
    session = get_object_or_404(AttendanceSession, id=session_id)
    
    if not session.is_active:
        return JsonResponse({'error': 'Sesi presensi sudah ditutup'}, status=400)
    
    # Cek apakah sudah presensi
    existing = AttendanceRecord.objects.filter(
        session=session, 
        student=request.user
    ).first()
    
    if existing:
        return JsonResponse({'error': 'Anda sudah presensi di sesi ini'}, status=400)
    
    # Buat record presensi
    status = request.POST.get('status', 'PRESENT')
    attendance = AttendanceRecord.objects.create(
        session=session,
        student=request.user,
        status=status
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Presensi berhasil dicatat',
        'status': attendance.get_status_display()
    })
