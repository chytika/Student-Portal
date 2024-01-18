from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    # notes
    path('notes/', views.notes_view, name="notes"),
    path('delete/<int:pk>', views.delete_note, name="delete_note"),
    path('edit/<int:pk>', views.edit_note, name="edit_note"),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name="NotesDetailView"),

    # Homework
    path('homework/', views.homework_view, name="homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),
    path('edit_homework/<int:pk>', views.edit_homework, name="edit-homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
      
    # Youtube
    path('youtube/', views.youtube, name="youtube"),

    # Todo
    path('todo/', views.todo, name="todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete-todo"),
    path('edit_todo/<int:pk>', views.edit_todo, name="edit-todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
      


]


