from django.shortcuts import render, redirect
from .forms import *
from .models import *
# from .models import Homework  
from django.contrib import messages
from django.views import generic



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

# NotesDetail page
class NotesDetailView(generic.DetailView):
    model = Notes


# Homework page
def homework_view(request):
     if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 0:
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished 
            )
            homeworks.save()
            messages.success(request,f'Homework added from {request.user.username} successfully!')
     else:
      form = HomeworkForm()

     homework = Homework.objects.filter(user=request.user)
     if len(homework) == 0:
        homework_done = True
     else:
        homework_done = False

     context = {
        'homework': homework,
        'homeworks_done': homework_done,
        'form': form,
     }
     return render(request, 'dashboard/homework.html', context)

# Delete homework
def delete_homework(request, pk=None):
    homework = Homework.objects.get(id=pk).delete()
    messages.success(request, f'Homework Deleted successfully!')
    return redirect('homework')



#  Edit homework
def edit_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)  
    if request.method == 'POST':
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == '0':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework.subject = request.POST['subject']
            homework.title = request.POST['title']
            homework.description = request.POST['description']
            homework.due = request.POST['due']
            homework.is_finished = finished
            homework.save()
            messages.success(request, f'Homework edited successfully!')
            return redirect('homework')
    else:
        form = HomeworkForm(instance=homework)

    context = {
        'form': form,
        'homework': homework,
    }

    return render(request, 'dashboard/edit_homework.html', context)



