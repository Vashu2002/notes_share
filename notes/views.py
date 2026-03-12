from django.shortcuts import render

def home(request):
    return render(request, 'notes/home.html')
def note_list(request):
    return render(request, 'notes_list/home.html')