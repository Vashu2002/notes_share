from django.db import models
from django.contrib.auth.models import User

# Choices for Institution Types
INSTITUTION_TYPES = (
    ('gov', 'Government'),
    ('pvt', 'Private'),
)

# --- 1. University ---
class University(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=INSTITUTION_TYPES, default='pvt')
    
    class Meta:
        verbose_name_plural = "Universities"

    def __str__(self): 
        return f"{self.name} ({self.get_type_display()})"

# --- 2. College ---
class College(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='colleges')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=INSTITUTION_TYPES, default='pvt')
    
    def __str__(self): 
        return f"{self.name} - {self.university.name}"

# --- 3. Course ---
class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    
    def __str__(self): 
        return f"{self.name} ({self.college.name})"

# --- 4. Semester ---
class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=50) 
    
    def __str__(self): 
        return f"{self.course.name} - {self.name}"

# --- 5. Batch ---
class Batch(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='batches')
    year = models.CharField(max_length=10) # e.g., 2024
    
    class Meta:
        verbose_name_plural = "Batches"

    def __str__(self): 
        return f"{self.semester} - {self.year}"

# --- 6. Note (The Core Model) ---
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='notes_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title