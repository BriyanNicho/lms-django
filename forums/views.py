from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from courses.models import Course
from .models import Thread, Reply

@login_required
def forum_list(request, course_id):
    """Tampilkan daftar topik diskusi dalam satu kelas"""
    course = get_object_or_404(Course, id=course_id)
    threads = course.threads.all().order_by('-created_at')
    
    context = {
        'course': course,
        'threads': threads,
    }
    
    return render(request, 'forums/forum_list.html', context)

@login_required
def thread_detail(request, thread_id):
    """Tampilkan detail topik dengan semua replies"""
    thread = get_object_or_404(Thread, id=thread_id)
    replies = thread.replies.all().order_by('created_at')
    
    context = {
        'thread': thread,
        'replies': replies,
        'reply_count': replies.count(),
    }
    
    return render(request, 'forums/thread_detail.html', context)

@login_required
@require_POST
def create_thread(request, course_id):
    """Buat topik diskusi baru"""
    course = get_object_or_404(Course, id=course_id)
    
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    if not title or not content:
        return JsonResponse({'error': 'Judul dan isi tidak boleh kosong'}, status=400)
    
    thread = Thread.objects.create(
        course=course,
        author=request.user,
        title=title,
        content=content
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Topik berhasil dibuat',
        'thread_id': thread.id,
        'redirect_url': f'/forum/thread/{thread.id}/'
    })

@login_required
@require_POST
def create_reply(request, thread_id):
    """Buat reply terhadap topik diskusi"""
    thread = get_object_or_404(Thread, id=thread_id)
    
    content = request.POST.get('content')
    
    if not content:
        return JsonResponse({'error': 'Isi balasan tidak boleh kosong'}, status=400)
    
    reply = Reply.objects.create(
        thread=thread,
        author=request.user,
        content=content
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Balasan berhasil ditambahkan',
        'author': reply.author.get_full_name() or reply.author.username,
        'created_at': reply.created_at.strftime('%d/%m/%Y %H:%M'),
    })
