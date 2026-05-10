from django.contrib import admin
from .models import Thread, Reply

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 1 # Menyediakan 1 kolom kosong untuk balasan baru

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
    list_display = ('title', 'course', 'author', 'created_at')

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply)