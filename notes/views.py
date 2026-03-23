from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from .models import Note, University, College, Course, Semester, Batch

# 🔹 1. Home Dashboard (User's own notes)
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'home.html'
    context_object_name = 'notes'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Search dropdowns ke liye data (Existing records)
        context['institutions'] = University.objects.all()
        context['batches'] = Batch.objects.all()
        return context

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')


# 🔹 2. AJAX Handlers (For Search Filter)
def load_courses(request):
    """Jab user University select kare, toh uske colleges ke courses load honge"""
    inst_id = request.GET.get('inst_id')
    courses = Course.objects.filter(college__university_id=inst_id).distinct().order_by('name')
    return JsonResponse(list(courses.values('id', 'name')), safe=False)


# 🔹 3. File Upload (The Knowledge Vault - Auto Hierarchy Logic)
@login_required(login_url='login')
def upload_note(request):
    if request.method == 'POST':
        # HTML form 'name' attributes se match kiya gaya hai
        title = request.POST.get('title')
        note_type = request.POST.get('note_type') # Handwritten, PYQ, etc.
        batch_year_val = request.POST.get('batch_year')
        inst_name = request.POST.get('institution_name')
        course_name = request.POST.get('course_name')
        file = request.FILES.get('note_file')

        # ✅ Basic Validation
        if not all([title, batch_year_val, inst_name, course_name, file]):
            messages.error(request, "⚠️ Please fill all fields!")
            return redirect('home')

        try:
            # --- START AUTO-CREATION CHAIN ---
            
            # 1. University Create/Get
            uni, _ = University.objects.get_or_create(name=inst_name)
            
            # 2. College Create/Get (Linking to University)
            col, _ = College.objects.get_or_create(
                name=f"{inst_name} Campus", 
                university=uni
            )
            
            # 3. Course Create/Get (Linking to College)
            course, _ = Course.objects.get_or_create(name=course_name, college=col)
            
            # 4. Semester Create/Get (Mandatory for Batch)
            sem, _ = Semester.objects.get_or_create(name="General", course=course)
            
            # 5. Batch Create/Get (Linking to Semester)
            batch, _ = Batch.objects.get_or_create(year=batch_year_val, semester=sem)

            # ✅ 6. Save Final Note
            # Note Type ko title mein merge kar rahe hain identification ke liye
            final_title = f"[{note_type.upper()}] {title}" if note_type else title
            
            Note.objects.create(
                user=request.user,
                batch=batch,
                title=final_title,
                file=file
            )

            messages.success(request, f"🚀 '{title}' has been vaulted successfully!")
            
        except Exception as e:
            messages.error(request, f"❌ System Error: {str(e)}")
            
        return redirect('home')

    return redirect('home')


# 🔹 4. Exploration & Discovery (Search Logic)
class ExploreNotesView(ListView):
    model = Note
    template_name = 'notes_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.all().order_by('-created_at')
        
        # Filter parameters from the search card
        inst_id = self.request.GET.get('institution')
        course_id = self.request.GET.get('course')
        batch_id = self.request.GET.get('batch')

        if inst_id:
            queryset = queryset.filter(batch__semester__course__college__university_id=inst_id)
        if course_id:
            queryset = queryset.filter(batch__semester__course_id=course_id)
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)

        return queryset


# 🔹 5. Static & Other Views
class LandingView(TemplateView):
    template_name = "landing.html"

class DiscoverView(ListView):
    model = Note
    template_name = 'explore.html'
    context_object_name = 'notes'
    def get_queryset(self):
        return Note.objects.all().order_by('-created_at')

class WalletView(LoginRequiredMixin, TemplateView):
    template_name = "wallet.html"

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"

class PrivacyView(TemplateView):
    template_name = "privacy_policy.html"