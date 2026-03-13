from django.db import models
from django.contrib.auth.models import User

# Type choice define kar sakte hain
INSTITUTION_TYPES = (
    ('gov', 'Government'),
    ('pvt', 'Private'),
)

class University(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=INSTITUTION_TYPES, default='pvt')
    
    def __str__(self): return f"{self.name} ({self.get_type_display()})"

class College(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=INSTITUTION_TYPES, default='pvt')
    
    def __str__(self): return f"{self.name} - {self.university.name}"

# Baki models mein koi change nahi chahiye
class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self): return f"{self.name} ({self.college.name})"

class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50) 
    def __str__(self): return f"{self.course.name} - {self.name}"

class Batch(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    year = models.CharField(max_length=10)
    def __str__(self): return f"{self.semester} - {self.year}"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True) # अगर सिर्फ फाइल है, तो content खाली हो सकता है
    file = models.FileField(upload_to='notes_files/', blank=True, null=True) # फाइल अपलोड के लिए
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title