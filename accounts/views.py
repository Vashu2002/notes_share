from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import EmailLoginForm, CustomSignUpForm

# 🔹 Auth Views
class MyLoginView(LoginView):
    template_name = 'accounts_auth/login.html'
    form_class = EmailLoginForm
    redirect_authenticated_user = True
    def get_success_url(self): return reverse_lazy('home')

class MyLogoutView(LogoutView): 
    next_page = reverse_lazy('landing')

class SignUpView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'accounts_auth/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # सिग्नल की वजह से प्रोफाइल पहले ही बन चुकी होगी
        response = super().form_valid(form)
        
        # यहाँ सिर्फ रोल अपडेट करें
        role = self.request.POST.get('user_role')
        if role:
            self.object.profile.role = role
            self.object.profile.save()
        return response