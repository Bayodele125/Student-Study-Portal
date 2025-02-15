from unittest import result
from django.views.generic import DetailView
from django.contrib import messages
from django.shortcuts import redirect, render
import requests
from .models import *
from .forms import *
from youtubesearchpython import VideosSearch
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'home.html')

@login_required
def notes(request):
    if request.method =="POST":
        form =NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user = request.user,title=request.POST['title'],description =request.POST['description'])
            notes.save()
        messages.success(request,f'Note Added from {request.user.username} Successfully!')
    else:
        form =NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(DetailView):
    model = Notes 
    

@login_required
def homework(request):
    if request.method == "POST":
        form =HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST('is_finished')
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                desciption= request.POST['desciption'],
                due= request.POST['due'],
                is_finished= finished
            )
            homeworks.save()
            messages.success(request,f'Homework Added From {request.user.username}!!')
    else:
        form = HomeworkForm()
    homework= Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks':homework,
        "homework_done":homework_done,
        "form":form
        }
    return render(request,'homework.html',context)

@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method == "POST":
        form =DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,10)
        result_list = []
        for i in video.result()['result']:
            result_dict ={
                'input':text,
                'video_id':i['id'],
                'title':i['title'],  
                'duration':i['duration'], 
                'thumbnails':i['thumbnails'][0]['url'],
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
                'form':form,
                'results':result_list
            }
        return render(request,'youtube.html',context)
    form = DashboardForm()
    context = {'form':form}
    return render(request, 'youtube.html',context)

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
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
            messages.success(request,f"Todo Added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'form':form,
        'todos':todo,
        'todo_done':todo_done
    } 
    return render(request,'todo.html',context)

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


def books(request):
    if request.method == "POST":
        form =DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        if r is None:
            message = f'{text} not found'
        else:
            answer = r.json()
            result_list = []
            for i in range(10):
                result_dict ={
                    'title':answer['items'][i]['volumeInfo']['title'], 
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'), 
                    'description':answer['items'][i]['volumeInfo'].get('description'), 
                    'count':answer['items'][i]['volumeInfo'].get('pageCount'), 
                    'categories':answer['items'][i]['volumeInfo'].get('categories'), 
                    'rating':answer['items'][i]['volumeInfo'].get('pageRating'), 
                    'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'), 
                    'preview':answer['items'][i]['volumeInfo'].get('previewLink') 
                }
                result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list,
                'message':message
            }
        return render(request,'books.html',context)
    form = DashboardForm()
    context = {'form':form}
    return render(request, 'books.html',context)


def dictionary(request):
    if request.method == "POST":
        form =DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
                'text':text
            }
            print(context)
        except KeyError:
            context = {
                'error':'THE TEXT WAS NOT FOUND IN OUR DATA BASE',
                'form':form,
            }
        return render(request,'dictionary.html',context)
    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,'dictionary.html',context)

@login_required
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        note = Notes.objects.filter(title__contains=searched)
        homework = Homework.objects.filter(title__contains=searched)
        todo = Todo.objects.filter(title__contains=searched)
        diary = Diary.objects.filter(date__contains=searched)
        if searched == '':
            messages.error(request,f'Hay!, you search for nothing!! {request.user}')
        result = (note,homework,todo)
        print(result)
        if result == '':
            messages.info(request,f'{searched} not found')
        return render(request,'search.html',{
            'searched':searched,
            'notes':note,
            'homeworks':homework,
            'todos':todo,
            'diary':diary 
        })
    else:    
        return render(request,'search.html',{'form':DashboardForm()})


def wiki(request):
    if request.method == "POST":
        search = request.POST['search']
        if search:
            result = wikipedia.page(search)
            context = {
                'title':result.title,
                'links':result.url,
                'details':result.summary
            }
            return render(request, 'wiki.html',context)
        else:
            messages.error(request, "Wrong Input")
        
    return render(request,'wiki.html')


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'inputs':True
            }
            if 'inputs' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                inputs = request.POST['inputs']
                answer = ''
                if inputs and int(inputs) >= 0:
                    if first == 'inch' and second == 'centimeter':
                        answer = f'{inputs} inch = {float(inputs)*2.54} cm'
                    if first == 'centimeter' and second == 'inch':
                        answer = f'{inputs} cm = {float(inputs)/2.54} inch'
                    if first == 'foot' and second == 'meter':
                        answer = f'{inputs} foot = {float(inputs)*0.3048} m'
                    if first == 'meter' and second == 'foot':
                        answer = f'{inputs} m = {float(inputs)/0.3048} foot'
                    if first == 'mile' and second == 'kilometer':
                        answer = f'{inputs} mile = {float(inputs)*1.60934} km'
                    if first == 'kilometer' and second == 'mile':
                        answer = f'{inputs} km = {float(inputs)/1.60934} mile'
                    if first == 'yard' and second == 'meter':
                        answer = f'{inputs} yard = {float(inputs)*0.9144} m'
                    if first == 'meter' and second == 'yard':
                        answer = f'{inputs} m = {float(inputs)/0.9144} yard'
                    if first == 'millimeter' and second == 'centimeter':
                        answer = f'{inputs} mm = {float(inputs)/10} cm'
                    if first == 'centimeter' and second == 'millimeter':
                        answer = f'{inputs} cm = {float(inputs)*10} mm'

                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'inputs':True,
                    'answer':answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'inputs':True
            }
            if 'inputs' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                inputs = request.POST['inputs']
                answer = ''
                if inputs and int(inputs) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{inputs} pound = {float(inputs)*0.453592} kg'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{inputs} kg = {float(inputs)*2.20462} pound'
                    if first == 'ounce' and second == 'gram':
                        answer = f'{inputs} oz = {float(inputs)*28.3495} g'
                    if first == 'gram' and second == 'ounce':
                        answer = f'{inputs} g = {float(inputs)/28.3495} oz'
                    if first == 'ton' and second == 'kilogram':
                        answer = f'{inputs} ton = {float(inputs)*907.185} kg'
                    if first == 'kilogram' and second == 'ton':
                        answer = f'{inputs} kg = {float(inputs)/907.185} ton'
                    if first == 'milligram' and second == 'gram':
                        answer = f'{inputs} mg = {float(inputs)/1000} g'
                    if first == 'gram' and second == 'milligram':
                        answer = f'{inputs} g = {float(inputs)*1000} mg'

                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'inputs':True,
                    'answer':answer
                }
    else:
        context = {
            'form':ConversionForm(),
            'inputs':False
        }
    return render(request, "conversion.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username} Successfully!!')
            return redirect("login")
    context = {
        'form':UserRegistrationForm()
    }
    return render(request,'register.html',context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context ={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }
    return render(request, 'profile.html',context)
