from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages



# Create your views here.

# Homepage
def home_view(request):
    return render(request, 'dashboard/home.html')


# Notes view
def notes_view(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            # notes.user = request.user
            notes.save()
        messages.success(request,f'Notes added from {request.user.username} successfully!')

    else:
        form = NotesForm()
            
    form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    # notes = Notes.objects.all()
    context = { 
        'notes': notes, 
        'form': form
    }
    return render(request, 'dashboard/notes.html', context)


# Delete Notes
def delete_note(request, pk=None):
   notes = Notes.objects.get(id=pk).delete()
   messages.success(request, f'Note Deleted successfully!')
   return redirect('notes')


#  Edit Notes
def edit_note(request, pk=None):
    note = Notes.objects.get(id=pk)  
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f'Note edited successfully!')
            return redirect('notes')
    else:
        form = NotesForm(instance=note)

    context = {
        'form': form,
        'note': note,
    }

    return render(request, 'dashboard/edit_note.html', context)

