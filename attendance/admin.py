from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord

class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0 # Tidak perlu kolom kosong otomatis
    readonly_fields = ('timestamp',) # Waktu absen tidak bisa diubah manual

class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'session_date', 'is_active')
    inlines = [AttendanceRecordInline]

admin.site.register(AttendanceSession, AttendanceSessionAdmin)
admin.site.register(AttendanceRecord)