from django.shortcuts import render
from . models import Notes

# Create your views here.


def home_view(request):
    return render(request, 'dashboard/home.html')


def notes_view(request):
    notes = Notes.objects.filter(user=request.user)
    context ={'notes': notes}
    return render(request, 'dashboard/notes.html', context)