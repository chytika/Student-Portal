from django.shortcuts import render
from . forms import *

# Create your views here.


def home_view(request):
    return render(request, 'dashboard/home.html')


def notes_view(request):
    form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = { 
        'notes': notes, 
        'form': form
    }
    return render(request, 'dashboard/notes.html', context)