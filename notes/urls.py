from django.urls import path
from . import views # views ko directly import karna zyada safe hai errors se bachne ke liye

urlpatterns = [
    # 🔹 Main Pages
    path('', views.LandingView.as_view(), name='landing'),
    path('home/', views.NoteListView.as_view(), name='home'),

    # 🔹 Upload (The Knowledge Vault)
    # Iska name 'upload_note' hi rakha hai jo HTML ke form action mein hai
    path('upload/', views.upload_note, name='upload_note'),

    # 🔹 AJAX (Search Filters ke liye)
    # HTML ke JS fetch(`/ajax/load-courses/?inst_id=${this.value}`) se match kiya gaya hai
    path('ajax/load-courses/', views.load_courses, name='load_courses'),

    # 🔹 Explore & Search Database
    # Jab user search button dabayega, wo is library path par jayega
    path('notes/library/', views.ExploreNotesView.as_view(), name='explore_notes'),
    path('discover/', views.DiscoverView.as_view(), name='explore_now'),
    path('home/discover/', views.DiscoverView.as_view(), name='home_explore'),

    # 🔹 Other Pages
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
]