from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from .models import Note, University, College, Course, Batch


# 🔹 Main Landing & Home
class LandingView(TemplateView):
    template_name = "landing.html"


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'home.html'
    context_object_name = 'notes'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['universities'] = University.objects.all()
        context['batches'] = Batch.objects.all()
        return context

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')


# 🔹 AJAX Handlers
def load_colleges(request):
    uni_id = request.GET.get('uni_id')
    colleges = College.objects.filter(university_id=uni_id).order_by('name')
    return JsonResponse(list(colleges.values('id', 'name')), safe=False)


def load_courses(request):
    col_id = request.GET.get('col_id')
    courses = Course.objects.filter(college_id=col_id).order_by('name')
    return JsonResponse(list(courses.values('id', 'name')), safe=False)


# 🔹 Exploration & Discovery
class ExploreNotesView(ListView):
    model = Note
    template_name = 'notes_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.all().order_by('-created_at')
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(batch__semester__course__name__icontains=query)
            )

        return queryset


class DiscoverView(ListView):
    model = Note
    template_name = 'explore.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Divine Knowledge Hub"
        context['page_subtitle'] = "Science is just a path, but scriptures and God are the destination."
        return context


# 🔹 Other Pages
class WalletView(LoginRequiredMixin, TemplateView):
    template_name = "wallet.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class PrivacyView(TemplateView):
    template_name = "privacy_policy.html"


# 🔹 File Upload (FINAL WORKING VERSION)
@login_required(login_url='login')
def upload_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        batch_id = request.POST.get('batch_id')
        file = request.FILES.get('note_file')

        # ✅ Validation
        if not title or not batch_id or not file:
            messages.error(request, "⚠️ All fields are required!")
            return redirect('home')

        # ✅ Safe batch fetch
        batch = get_object_or_404(Batch, id=batch_id)

        # ✅ File type validation
        allowed_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/png'
        ]

        if file.content_type not in allowed_types:
            messages.error(request, "❌ Only PDF, DOCX, JPG, PNG allowed!")
            return redirect('home')

        # ✅ Save note
        Note.objects.create(
            user=request.user,
            batch=batch,
            title=title,
            file=file
        )

        messages.success(request, "✅ Note uploaded successfully!")
        return redirect('home')

    return redirect('home')