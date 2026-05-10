from django.contrib import admin
from django.urls import path
from accounts import views as account_views
from courses import views as course_views
from assessments import views as assessment_views
from attendance import views as attendance_views
from forums import views as forum_views

urlpatterns = [
    # Auth URLs
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('register/', account_views.register_view, name='register'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Dashboard
    path('', account_views.dashboard, name='dashboard'),
    
    # Course URLs
    path('course/<int:course_id>/', course_views.course_detail, name='course_detail'),
    path('course/<int:course_id>/materials/', course_views.course_materials, name='course_materials'),
    
    # Attendance URLs
    path('course/<int:course_id>/attendance/', attendance_views.attendance_list, name='attendance_list'),
    path('attendance/<int:session_id>/', attendance_views.attendance_session_detail, name='attendance_detail'),
    path('attendance/<int:session_id>/mark/', attendance_views.mark_attendance, name='mark_attendance'),
    
    # Assignment & Quiz URLs
    path('course/<int:course_id>/assignments/', assessment_views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/', assessment_views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', assessment_views.submit_assignment, name='submit_assignment'),
    
    path('course/<int:course_id>/quizzes/', assessment_views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', assessment_views.quiz_detail, name='quiz_detail'),
    
    # Forum URLs
    path('course/<int:course_id>/forum/', forum_views.forum_list, name='forum_list'),
    path('thread/<int:thread_id>/', forum_views.thread_detail, name='thread_detail'),
    path('course/<int:course_id>/forum/create/', forum_views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/reply/', forum_views.create_reply, name='create_reply'),
]