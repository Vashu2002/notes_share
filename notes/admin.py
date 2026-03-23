from django.contrib import admin
from .models import University, College, Course, Semester, Batch, Note

# --- 1. University Admin ---
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type') 
    list_filter = ('type',)
    search_fields = ('name',)

# --- 2. College Admin ---
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'type')
    list_filter = ('type', 'university')
    search_fields = ('name', 'university__name')

# --- 3. Course Admin ---
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'college')
    # Filter by university (via college)
    list_filter = ('college__university', 'college')
    search_fields = ('name', 'college__name')

# --- 4. Semester Admin ---
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course__college__university', 'course')
    search_fields = ('name', 'course__name')

# --- 5. Batch Admin ---
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('year', 'semester')
    list_filter = ('year', 'semester__course')
    search_fields = ('year', 'semester__name', 'semester__course__name')

# --- 6. Note Admin (Master Controller) ---
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # list_display mein wo important info jo admin ko turant chahiye
    list_display = ('title', 'user', 'get_institution', 'get_course', 'batch', 'created_at')
    
    # Powerful Search: Ab aap Uni name, Course name ya Username se dhoond sakte ho
    search_fields = (
        'title', 
        'user__username', 
        'batch__semester__course__name', 
        'batch__semester__course__college__university__name'
    )
    
    # Sidebar Filters ko useful banaya hai
    list_filter = (
        'created_at', 
        'batch__year', 
        'batch__semester__course__college__university'
    )
    
    # Timeline view ke liye
    date_hierarchy = 'created_at'

    # Custom methods taaki list view mein hi pata chal jaye note kahan ka hai
    def get_institution(self, obj):
        return obj.batch.semester.course.college.university.name
    get_institution.short_description = 'University'

    def get_course(self, obj):
        return obj.batch.semester.course.name
    get_course.short_description = 'Course'