from django.shortcuts import render, redirect
from .forms import *
from .models import *
# from .models import Homework  
from django.contrib import messages
from django.views import generic
from django.forms.widgets import FileInput
from youtubesearchpython import VideosSearch


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

#  Update homework
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk) 
    if  homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

# # Youtube
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []


        for i in video.result()['result']:
            result_dict = {
                 'input':text,
                 'title':i['title'],
                 'duration':i['duration'],
                 'thumbnail':i['thumbnails'][0]['url'],
                 'channel':i['channel']['name'],
                 'link':i['link'],
                 'views':i['viewCount']['short'],
                 'published':i['publishedTime'],
            }

            desc =''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        context = {
             'form': form,
             'results': result_list,
        }
        return render(request, 'dashboard/youtube.html',context)


    else:
     form = DashboardForm()
    context = {
        'form': form,
        # 'homework': homework,
    }
    return render(request, 'dashboard/youtube.html',context)

# Todo
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 0:
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f'Todo added from {request.user.username} successfully!')
    else:
      form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    
    context = {
        'todos':todo,
        'todos_done': todo_done,
        'form': form,

    }
    return render(request, 'dashboard/todo.html', context)

 # Delete Todo
def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk).delete()
    messages.success(request, f'Todo Deleted successfully!')
    return redirect('todo')    
            
 
#  Edit todo
def edit_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)  
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == '0':
                    finished = True
                else:
                    finished = False
            except:
                finished = False               
            todo.title = request.POST['title'],
            todo.is_finished = finished
            todo.save()
            messages.success(request, f'Todo edited successfully!')
            return redirect('todo')
    else:
        form = TodoForm(instance=todo)
    context = {
        'form': form,
        'todo': todo,
    }

    return render(request, 'dashboard/edit_todo.html', context)

  #  Update homework
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk) 
    if  todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')