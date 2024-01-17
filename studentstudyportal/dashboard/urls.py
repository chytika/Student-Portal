from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('notes/', views.notes_view, name="notes"),
    path('delete/<int:pk>', views.delete_note, name="delete_note"),
    path('edit/<int:pk>', views.edit_note, name="edit_note"),
]
