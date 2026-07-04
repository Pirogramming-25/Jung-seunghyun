from django.shortcuts import render, redirect, get_object_or_404
from . forms import DevToolForm, IdeaForm
from . models import DevTool, Idea, IdeaStar
from django.http import JsonResponse
import json
# Create your views here.

def get_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devtool_list')
    else:
        form = DevToolForm()
    return render(request, 'ideas/devtool_form.html', {'form': form})

def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'ideas/devtool_list.html', {'devtools': devtools})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)    
    ideas = devtool.idea_set.all()
    return render(request, 'ideas/devtool_detail.html', {'devtool': devtool, 'ideas': ideas})

def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('devtool_list')

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            form.save()
            return redirect('devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, 'ideas/devtool_form.html', {'form': form})

def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('idea_list')
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_form.html', {'form': form})

def idea_list(request):
    sort = request.GET.get('sort', 'new')
    
    if sort == 'name':
        ideas = Idea.objects.all().order_by('title')
    elif sort == 'old':
        ideas = Idea.objects.all().order_by('created_at')
    else:
        ideas = Idea.objects.all().order_by('-created_at')

    return render(request, 'ideas/idea_list.html', {'ideas': ideas, 'sort': sort})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    session_key = get_session_key(request)
    is_starred = IdeaStar.objects.filter(idea=idea, session_key=session_key).exists()
    return render(request, 'ideas/idea_detail.html', {'idea': idea, 'is_starred': is_starred})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('idea_list')

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'ideas/idea_form.html', {'form': form})


from .models import DevTool, Idea, IdeaStar

def idea_star_toggle(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    session_key = get_session_key(request)

    star = IdeaStar.objects.filter(idea=idea, session_key=session_key).first()

    if star:
        star.delete()
        starred = False
    else:
        IdeaStar.objects.create(idea=idea, session_key=session_key)
        starred = True

    return JsonResponse({'starred': starred})

def idea_interest_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    data = json.loads(request.body)
    delta = data.get('delta')

    idea.interest += delta
    idea.save()

    return JsonResponse({'interest': idea.interest})