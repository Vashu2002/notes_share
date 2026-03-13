from django.contrib import admin
from .models import University, College, Course, Semester, Batch, Note

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    # 'is_government' ki jagah ab 'type' use hoga
    list_display = ('name', 'type') 
    list_filter = ('type',)

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    # 'type' field ab College model mein bhi hai
    list_display = ('name', 'university', 'type')
    list_filter = ('type', 'university')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'college')
    list_filter = ('college',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('year', 'semester')
    list_filter = ('semester',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'batch', 'created_at')
    search_fields = ('title', 'batch__semester__course__name')
    list_filter = ('batch', 'created_at')