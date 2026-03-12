from django.urls import path
from .views import (
    LandingView, MyLoginView, MyLogoutView, SignUpView,
    NoteListView, AboutView, ContactView, ExploreNotesView, 
    DiscoverView, WalletView, PrivacyView
)

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('home/', NoteListView.as_view(), name='home'),
    
    # 🔹 Navbar Link (Normal Library)
    path('notes/library/', ExploreNotesView.as_view(), name='explore_notes'), 

    # 🔹 Explore/Discover (Home & Landing Buttons)
    # Dono ko 'DiscoverView' par bhej rahe hain kyunki aapko alag kaam chahiye
    path('discover/', DiscoverView.as_view(), name='explore_now'),    
    path('home/discover/', DiscoverView.as_view(), name='home_explore'), 
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # Others
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
]