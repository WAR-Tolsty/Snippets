from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)

@login_required(login_url='home')
def add_snippet_page(request):

    if request.method == "GET":
        form  = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form,
        }
        return render(request, 'pages/add_snippet.html', context)
    
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                form.save()
            return redirect("snippets-list")
        return render(request, "pages/add_snippet.html", {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id: int):
    context = {"pagename": "Просмотр сниппета"}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return render(request, "pages/errors.html", context | {"error": f'Snippet with id={snippet_id} not found'})
    else:
        
        context["snippet"] = snippet
        context['type'] = 'view'
        
        return render(request, "pages/snippet_detail.html", context)
    
def snippet_edit(request, snippet_id: int):
    context = {"pagename": "Редактирование сниппета"}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return Http404
    
    if request.method == 'GET':
        form = SnippetForm(instance=snippet)
        return render(request, 'pages/add_snippet.html', {'form': form})


    #if request.method == "GET":
    #    context = {
    #        'snippet': snippet,
    #        'type': 'edit'
    #    }
    #    return render(request, 'pages/snippet_detail.html', context)
    
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form['name']
        snippet.code = data_form['code']
        snippet.save()
        return redirect('snippets-list')

def snippet_delete(request, snippet_id: int):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    snippet.delete()
    return redirect('snippets-list')

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username,
        password=password)
    if user is not None:
        auth.login(request, user)
    else:
        context = {
            "pagename": "PythonBin",
            "errors": ['Wrong username or password'],
        }
        return render(request, "pages/index.html", context)
    return redirect('home')

def logout(request):
    auth.logout(request)
    return redirect('home')