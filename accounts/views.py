from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Q
from .forms import EmailLoginForm, CustomSignUpForm
from .models import Note

# 🔹 1. Main Landing & Home
class LandingView(TemplateView):
    template_name = "landing.html"

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'home.html'
    context_object_name = 'notes'
    login_url = 'login'
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

# 🔹 2. Navbar "Notes" View (Normal Library)
class ExploreNotesView(ListView):
    model = Note
    template_name = 'explore.html'  # Isme normal list wala code rakhein
    context_object_name = 'notes'
    
    def get_queryset(self):
        queryset = Note.objects.all().order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(subject__icontains=query))
        return queryset

# 🔹 3. Home/Landing "Explore Now" View (Scriptural/Premium Look)
class DiscoverView(ListView):
    model = Note
    template_name = 'explore.html'  # Ek nayi file banayein discover.html naam se
    context_object_name = 'notes'

    def get_queryset(self):
        # Yahan hum featured ya high-quality notes dikha sakte hain
        return Note.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aapka core logic yahan context mein jayega
        context['page_title'] = "Divine Knowledge Hub"
        context['page_subtitle'] = "Science is just a path, but scriptures and God are the destination."
        return context

# 🔹 4. Auth & Static Views
class MyLoginView(LoginView):
    template_name = 'accounts_auth/login.html'
    form_class = EmailLoginForm
    redirect_authenticated_user = True
    def get_success_url(self): return reverse_lazy('home')

class MyLogoutView(LogoutView): next_page = reverse_lazy('landing')

class SignUpView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'accounts_auth/signup.html'
    success_url = reverse_lazy('login')

class WalletView(LoginRequiredMixin, TemplateView): template_name = "wallet.html"
class AboutView(TemplateView): template_name = "about.html"
class ContactView(TemplateView): template_name = "contact.html"
class PrivacyView(TemplateView): template_name = "privacy_policy.html"



