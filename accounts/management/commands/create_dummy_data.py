from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from courses.models import Course, Material
from assessments.models import Assignment, Submission, Quiz, Question
from attendance.models import AttendanceSession, AttendanceRecord
from forums.models import Thread, Reply


class Command(BaseCommand):
    help = 'Create dummy data for testing LMS application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting to create dummy data...'))

        # Clear existing data
        self.clear_existing_data()

        # Create users
        admin, teachers, students = self.create_users()

        # Create courses
        courses = self.create_courses(teachers)

        # Create materials
        self.create_materials(courses)

        # Create assignments
        assignments = self.create_assignments(courses)

        # Create submissions
        self.create_submissions(assignments, students)

        # Create quizzes & questions
        quizzes = self.create_quizzes(courses)

        # Create attendance sessions & records
        self.create_attendance(courses, students)

        # Create forum threads & replies
        self.create_forum(courses, students)

        self.stdout.write(self.style.SUCCESS('✅ Dummy data created successfully!'))
        self.print_credentials()

    def clear_existing_data(self):
        """Clear existing data (optional)"""
        self.stdout.write('🧹 Clearing existing data...')
        # Jangan delete semua, hanya optional

    def create_users(self):
        """Create dummy users"""
        self.stdout.write('👥 Creating users...')

        # Admin
        admin, _ = User.objects.get_or_create(
            username='admin1',
            defaults={
                'email': 'admin@lms.local',
                'first_name': 'Admin',
                'last_name': 'System',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if not admin.has_usable_password() or admin.password.startswith('pbkdf2'):
            admin.set_password('password123')
            admin.save()

        # Teachers
        teachers = []
        teacher_names = [
            ('Budi', 'Santoso'),
            ('Siti', 'Nurhaliza'),
            ('Ahmad', 'Wijaya'),
        ]

        for i, (first, last) in enumerate(teacher_names, 1):
            teacher, _ = User.objects.get_or_create(
                username=f'teacher{i}',
                defaults={
                    'email': f'teacher{i}@lms.local',
                    'first_name': first,
                    'last_name': last,
                    'role': 'TEACHER',
                }
            )
            if not teacher.has_usable_password() or teacher.password.startswith('pbkdf2'):
                teacher.set_password('password123')
                teacher.save()
            teachers.append(teacher)

        # Students
        students = []
        student_names = [
            ('Andi', 'Pratama'),
            ('Bella', 'Kusuma'),
            ('Citra', 'Dewi'),
            ('Doni', 'Setiawan'),
            ('Eka', 'Putri'),
            ('Fajar', 'Rahman'),
        ]

        for i, (first, last) in enumerate(student_names, 1):
            student, _ = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@lms.local',
                    'first_name': first,
                    'last_name': last,
                    'role': 'STUDENT',
                }
            )
            if not student.has_usable_password() or student.password.startswith('pbkdf2'):
                student.set_password('password123')
                student.save()
            students.append(student)

        self.stdout.write(f'  ✓ Created {len(teachers)} teachers and {len(students)} students')
        return admin, teachers, students

    def create_courses(self, teachers):
        """Create dummy courses"""
        self.stdout.write('📚 Creating courses...')

        courses_data = [
            {
                'title': 'Pemrograman Python',
                'description': 'Kursus dasar pembelajaran bahasa pemrograman Python untuk pemula hingga menengah.',
                'teacher': teachers[0],
            },
            {
                'title': 'Web Development dengan Django',
                'description': 'Belajar membuat aplikasi web modern menggunakan Django framework.',
                'teacher': teachers[0],
            },
            {
                'title': 'Database MySQL',
                'description': 'Pengenalan dan praktik menggunakan MySQL database untuk aplikasi profesional.',
                'teacher': teachers[1],
            },
            {
                'title': 'Frontend React',
                'description': 'Kuasai React untuk membuat user interface yang interaktif dan responsif.',
                'teacher': teachers[1],
            },
            {
                'title': 'Mobile Development',
                'description': 'Pelajari development aplikasi mobile dengan Flutter dan React Native.',
                'teacher': teachers[2],
            },
        ]

        courses = []
        for course_data in courses_data:
            course, _ = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'teacher': course_data['teacher'],
                }
            )
            courses.append(course)

        self.stdout.write(f'  ✓ Created {len(courses)} courses')
        return courses

    def create_materials(self, courses):
        """Create dummy materials"""
        self.stdout.write('📖 Creating materials...')

        materials_count = 0

        for course in courses:
            materials_data = [
                {
                    'title': f'Pengenalan {course.title}',
                    'material_type': 'PDF',
                    'content_url': 'https://example.com/intro.pdf',
                },
                {
                    'title': f'Tutorial Video {course.title}',
                    'material_type': 'VIDEO',
                    'content_url': 'https://www.youtube.com/watch?v=example',
                },
                {
                    'title': f'Slide Presentasi {course.title}',
                    'material_type': 'PPT',
                    'content_url': 'https://example.com/slides.pptx',
                },
                {
                    'title': f'Dokumentasi {course.title}',
                    'material_type': 'LINK',
                    'content_url': 'https://docs.example.com',
                },
            ]

            for material_data in materials_data:
                Material.objects.get_or_create(
                    course=course,
                    title=material_data['title'],
                    defaults={
                        'material_type': material_data['material_type'],
                        'content_url': material_data['content_url'],
                    }
                )
                materials_count += 1

        self.stdout.write(f'  ✓ Created {materials_count} materials')

    def create_assignments(self, courses):
        """Create dummy assignments"""
        self.stdout.write('✏️  Creating assignments...')

        assignments = []
        now = timezone.now()

        for course in courses:
            assignments_data = [
                {
                    'title': f'Tugas 1: Introduksi {course.title}',
                    'description': 'Kerjakan soal-soal introduction yang telah diberikan di kelas.',
                    'due_date': now + timedelta(days=7),
                },
                {
                    'title': f'Tugas 2: Praktik Coding {course.title}',
                    'description': 'Buat project kecil sesuai dengan materi yang telah dipelajari.',
                    'due_date': now + timedelta(days=14),
                },
                {
                    'title': f'Tugas 3: Mini Project {course.title}',
                    'description': 'Buat project yang menggunakan semua konsep yang sudah dipelajari.',
                    'due_date': now + timedelta(days=21),
                },
            ]

            for assignment_data in assignments_data:
                assignment, _ = Assignment.objects.get_or_create(
                    course=course,
                    title=assignment_data['title'],
                    defaults={
                        'description': assignment_data['description'],
                        'due_date': assignment_data['due_date'],
                    }
                )
                assignments.append(assignment)

        self.stdout.write(f'  ✓ Created {len(assignments)} assignments')
        return assignments

    def create_submissions(self, assignments, students):
        """Create dummy submissions"""
        self.stdout.write('📤 Creating submissions...')

        submission_count = 0
        now = timezone.now()

        for assignment in assignments[:5]:  # Hanya untuk beberapa assignment
            for student in students[:4]:  # Hanya untuk beberapa student
                submission, _ = Submission.objects.get_or_create(
                    assignment=assignment,
                    student=student,
                    defaults={
                        'submitted_at': now - timedelta(days=2),
                        'grade': None,
                        'feedback': None,
                    }
                )
                submission_count += 1

        self.stdout.write(f'  ✓ Created {submission_count} submissions')

    def create_quizzes(self, courses):
        """Create dummy quizzes with questions"""
        self.stdout.write('❓ Creating quizzes and questions...')

        quizzes = []
        now = timezone.now()

        for course in courses:
            quiz, _ = Quiz.objects.get_or_create(
                course=course,
                title=f'Kuis {course.title}',
                defaults={
                    'due_date': now + timedelta(days=10),
                }
            )
            quizzes.append(quiz)

            # Create questions for this quiz
            questions_data = [
                {
                    'text': 'Apa pengertian dari konsep utama dalam topik ini?',
                    'option_a': 'Definisi A',
                    'option_b': 'Definisi B',
                    'option_c': 'Definisi C (Benar)',
                    'option_d': 'Definisi D',
                    'correct_answer': 'C',
                },
                {
                    'text': 'Konsep mana yang paling penting diaplikasikan?',
                    'option_a': 'Konsep 1',
                    'option_b': 'Konsep 2 (Benar)',
                    'option_c': 'Konsep 3',
                    'option_d': 'Konsep 4',
                    'correct_answer': 'B',
                },
                {
                    'text': 'Bagaimana cara terbaik mengimplementasikan ini?',
                    'option_a': 'Cara 1 (Benar)',
                    'option_b': 'Cara 2',
                    'option_c': 'Cara 3',
                    'option_d': 'Cara 4',
                    'correct_answer': 'A',
                },
                {
                    'text': 'Apa keuntungan utama dari pendekatan ini?',
                    'option_a': 'Keuntungan 1',
                    'option_b': 'Keuntungan 2',
                    'option_c': 'Keuntungan 3',
                    'option_d': 'Keuntungan 4 (Benar)',
                    'correct_answer': 'D',
                },
                {
                    'text': 'Kapan sebaiknya menggunakan teknik ini?',
                    'option_a': 'Waktu 1',
                    'option_b': 'Waktu 2 (Benar)',
                    'option_c': 'Waktu 3',
                    'option_d': 'Waktu 4',
                    'correct_answer': 'B',
                },
            ]

            for q_data in questions_data:
                Question.objects.get_or_create(
                    quiz=quiz,
                    text=q_data['text'],
                    defaults={
                        'option_a': q_data['option_a'],
                        'option_b': q_data['option_b'],
                        'option_c': q_data['option_c'],
                        'option_d': q_data['option_d'],
                        'correct_answer': q_data['correct_answer'],
                    }
                )

        self.stdout.write(f'  ✓ Created {len(quizzes)} quizzes with questions')
        return quizzes

    def create_attendance(self, courses, students):
        """Create dummy attendance sessions and records"""
        self.stdout.write('✅ Creating attendance sessions...')

        session_count = 0
        record_count = 0
        now = timezone.now()

        for course in courses:
            for i in range(1, 4):  # 3 sesi per course
                session_date = now - timedelta(days=5-i)
                session, _ = AttendanceSession.objects.get_or_create(
                    course=course,
                    session_date=session_date.date(),
                    defaults={
                        'start_time': timezone.make_aware(timezone.datetime.strptime('09:00', '%H:%M')).time(),
                        'end_time': timezone.make_aware(timezone.datetime.strptime('11:00', '%H:%M')).time(),
                        'is_active': i == 3,  # Hanya sesi terakhir yang aktif
                    }
                )
                session_count += 1

                # Create attendance records
                for student in students[:5]:
                    status_choices = ['PRESENT', 'PRESENT', 'LATE', 'ABSENT']
                    status = status_choices[students.index(student) % len(status_choices)]

                    AttendanceRecord.objects.get_or_create(
                        session=session,
                        student=student,
                        defaults={
                            'status': status,
                        }
                    )
                    record_count += 1

        self.stdout.write(f'  ✓ Created {session_count} sessions and {record_count} attendance records')

    def create_forum(self, courses, students):
        """Create dummy forum threads and replies"""
        self.stdout.write('💬 Creating forum threads and replies...')

        thread_count = 0
        reply_count = 0

        for course in courses[:3]:  # Hanya untuk 3 courses
            threads_data = [
                {
                    'title': 'Pertanyaan tentang materi minggu pertama',
                    'content': 'Saya tidak begitu mengerti tentang konsep X. Bisakah dijelaskan lebih detail?',
                    'author': students[0],
                },
                {
                    'title': 'Tips dan trik mengerjakan tugas',
                    'content': 'Ini adalah beberapa tips yang saya temukan saat mengerjakan tugas.',
                    'author': students[1],
                },
                {
                    'title': 'Diskusi tentang project final',
                    'content': 'Mari kita diskusikan ide-ide untuk project final yang akan datang.',
                    'author': students[2],
                },
            ]

            for thread_data in threads_data:
                thread, _ = Thread.objects.get_or_create(
                    course=course,
                    title=thread_data['title'],
                    defaults={
                        'content': thread_data['content'],
                        'author': thread_data['author'],
                    }
                )
                thread_count += 1

                # Create replies
                replies_data = [
                    'Terima kasih atas penjelasannya!',
                    'Saya setuju dengan pendapat Anda.',
                    'Ada yang punya solusi lain?',
                    'Bagus sekali tipsnya!',
                ]

                for reply_text in replies_data:
                    reply, _ = Reply.objects.get_or_create(
                        thread=thread,
                        author=students[(students.index(thread_data['author']) + 1) % len(students)],
                        content=reply_text,
                    )
                    reply_count += 1

        self.stdout.write(f'  ✓ Created {thread_count} threads and {reply_count} replies')

    def print_credentials(self):
        """Print credentials for login"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📋 LOGIN CREDENTIALS'))
        self.stdout.write('='*60)
        self.stdout.write('\n🔐 Admin Account:')
        self.stdout.write('   Username: admin1')
        self.stdout.write('   Password: password123')

        self.stdout.write('\n👨‍🏫 Teacher Accounts:')
        self.stdout.write('   Username: teacher1, teacher2, teacher3')
        self.stdout.write('   Password: password123')

        self.stdout.write('\n👨‍🎓 Student Accounts:')
        self.stdout.write('   Username: student1, student2, student3, student4, student5, student6')
        self.stdout.write('   Password: password123')

        self.stdout.write('\n🌐 Access URL:')
        self.stdout.write('   http://localhost:8001/login/')

        self.stdout.write('\n' + '='*60 + '\n')
