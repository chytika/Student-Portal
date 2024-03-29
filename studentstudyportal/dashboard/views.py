from django.shortcuts import render, redirect
from .forms import *
from .models import *
# from .models import Homework  
from django.contrib import messages
from django.views import generic
from django.forms.widgets import FileInput
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required 





# Create your views here.

# Homepage
def home_view(request):
    return render(request, 'dashboard/home.html')


# Notes view
@login_required
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
    # notes = Notes.objects.filter(user=request.user)
    notes = Notes.objects.all()
    context = { 
        'notes': notes, 
        'form': form
    }
    return render(request, 'dashboard/notes.html', context)


# Delete Notes
@login_required
def delete_note(request, pk=None):
   notes = Notes.objects.get(id=pk).delete()
   messages.success(request, f'Note Deleted successfully!')
   return redirect('notes')


#  Edit Notes
@login_required
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
@login_required  
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
@login_required
def delete_homework(request, pk=None):
    homework = Homework.objects.get(id=pk).delete()
    messages.success(request, f'Homework Deleted successfully!')
    return redirect('homework')

#  Edit homework
@login_required
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
@login_required
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
@login_required
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
    # todo = Todo.objects.all()
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
@login_required
def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk).delete()
    messages.success(request, f'Todo Deleted successfully!')
    return redirect('todo')    
            
#  Edit todo
@login_required
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
@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk) 
    if  todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')


# Books
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
                 
            }
            result_list.append(result_dict)
            context = {
             'form': form,
             'results': result_list,
            }
        return render(request, 'dashboard/books.html',context)
    
    form = DashboardForm()
    context = {
        'form': form,
        
    }
    return render(request,'dashboard/books.html', context)


# # Dictionary
def dictionary(request):
     if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text'] 
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        # print(answer)  # Print the API response for debugging

        try:
           phonetics = answer[0]['phonetics'][0]['text']
           audio = answer[0]['phonetics'][0]['audio']
           definition = answer[0]['meanings'][0]['definitions'][0]['definition']
           example = answer[0]['meanings'][0]['definitions'][0]['example']
           synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

           context = {
                 'form': form,
                 'input':text,
                 'phonetics': phonetics,
                 'audio': audio,
                 'definition': definition,
                 'example': example,
                 'synonyms': synonyms,  
             }
        except:
            context = {
                'form': form,
                 'input':'',
            }
        return render(request,'dashboard/dictionary.html', context) 
     
     else:
        form = DashboardForm()
        context = {'form': form }
     return render(request,'dashboard/dictionary.html', context)
    
 # wiki
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context ={
            'form': form,
            'title': search.title,
            # 'link': search.url,
            'link': search.links,
            'details': search.summary
        }
        return render(request, 'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
        context = {'form': form }
    return render(request, 'dashboard/wiki.html',context)


 # conversion
def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second =='foot':
                        answer = f'{input} yard ={int(input)*3} foot'
                    if first == 'foot' and second =='yard':
                        answer = f'{input} foot ={int(input)/3} yard'
                context ={
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                    
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second =='kilogram':
                        answer = f'{input} pound ={int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second =='pound':
                        answer = f'{input} kilogram ={int(input)*2.20462} pound'
                context ={
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer   
                }
    else:
        form = ConversionForm()
        context = {
            'form': form ,
            'input':False
        }
    return render(request, 'dashboard/conversion.html', context)

# user_register
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f'Account Created for {username}!!')
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
            'form': form 
        }
    return render(request, 'dashboard/register.html',context)

# profile
@login_required
def profile(request):
     homework = Homework.objects.filter(user=request.user)
     todo = Todo.objects.filter(user=request.user)
     if len(homework) == 0:
        homework_done = True
     else:
        homework_done = False
     if len(todo) == 0:
        todo_done = True
     else:
        todo_done = False
     context = {
        'homework': homework,
        'homeworks_done': homework_done,
         'todos':todo,
        'todos_done': todo_done,
    }
     return render(request,"dashboard/profile.html",context)