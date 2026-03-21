from django.urls import path
from .views import (
    LandingView, NoteListView, AboutView, ContactView, 
    ExploreNotesView, DiscoverView, WalletView, PrivacyView,
    load_colleges, load_courses, upload_note
)

urlpatterns = [
    # 🔹 Main Pages
    path('', LandingView.as_view(), name='landing'),
    path('home/', NoteListView.as_view(), name='home'),

    # 🔹 Upload
    path('upload/', upload_note, name='upload_note'),

    # 🔹 AJAX
    path('ajax/load-colleges/', load_colleges, name='load_colleges'),
    path('ajax/load-courses/', load_courses, name='load_courses'),

    # 🔹 Explore
    path('notes/library/', ExploreNotesView.as_view(), name='explore_notes'),
    path('discover/', DiscoverView.as_view(), name='explore_now'),
    path('home/discover/', DiscoverView.as_view(), name='home_explore'),

    # 🔹 Other Pages
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
]