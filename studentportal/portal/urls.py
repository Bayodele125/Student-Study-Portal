from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    #Notes section
    path('notes',views.notes,name='notes'),
    path('delete_note/<int:pk>',views.delete_note,name='delete_note'),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(template_name = 'notes_detail.html'),name='notes_detail'),
    
    #homework section
    path('homework',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>',views.delete_homework,name='delete_homework'),

    #youtube
    path('youtube',views.youtube,name='youtube'),    
    
    #todo
    path('todo',views.todo,name='todo'),    
    path('update_todo/<int:pk>',views.update_todo,name='update_todo'), 
    path('delete_todo/<int:pk>',views.delete_todo,name='delete_todo'),

    #books
    path('books',views.books,name='books'),

    #dictionary    
    path('dictionary',views.dictionary,name='dictionary'),

    #search
    path('search',views.search,name='search'),

    #wikipedia
    path('wikipedia', views.wiki, name='wikipedia'),

    #conversion
    path('conversion', views.conversion, name='conversion'),

    # ASKAI
    path('askai', views.askAI, name='askAI'),
]