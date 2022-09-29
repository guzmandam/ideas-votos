from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from . import forms, models

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('votos:list'))
    return render(
        request,
        'votos/index.html'
    )

def signup(request):
    user_form = forms.SignupUserForm()
    context_dict = {
        'userForm': user_form
    }
    if request.method == 'POST':
        user_form = forms.SignupUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            return HttpResponseRedirect(reverse('votos:login'))
        
    return render(
        request,
        'votos/signup.html',
        context=context_dict
    )

def signup_staff(request):
    if request.user.is_superuser:
        staff_form = forms.SignupStaffForm()
        if request.method == 'POST':
            staff_form = forms.SignupStaffForm(request.POST)
            if staff_form.is_valid():
                staff_user = staff_form.save(commit=False)
                staff_user.is_staff = True
                staff_user.save()
                
                message = f'{staff_user.username} fue agregado como miembro staff exitosamente!'
                messages.success(request, message)
                return HttpResponseRedirect(reverse('votos:login'))
        context_dict = {
            'staffForm': staff_form
        }
        return render(
            request,
            'votos/signup_staff.html'
        )
    return render(
        request,
        'votos/404.html'
    )

# @login_required
# def user(request):

@login_required
def list_polls(request):
    all_polls = models.Poll.objects.all()
    search_term = ''
    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')

    if 'vote' in request.GET:
        all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6) 
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    context = {
        'polls': polls,
        'params': params,
        'searchTerm': search_term,
    }
    return render(request, 'votos/votaciones.html', context)

@staff_member_required(login_url='votos:login')
def add_poll(request):
    if request.method == 'POST':
        poll_form = forms.AddPollForm(request.POST)
        if poll_form.is_valid:
            poll = poll_form.save(commit=False)
            poll.owner = request.user
            poll.save()
            
            models.Choice(
                poll=poll, choice_text=poll_form.cleaned_data['choice1']).save()
            models.Choice(
                poll=poll, choice_text=poll_form.cleaned_data['choice2']).save()
            
            messages.success(
                request, 
                "Votacion y opciones agregadas correctamente!", 
                extra_tags='alert alert-success alert-dismissible fade show')
            
            return HttpResponseRedirect(reverse('votos:list'))
    else:
        poll_form = forms.AddPollForm()
        context_dict = {
            'pollForm': poll_form
        }
        return render(
            request,
            'votos/agregar_votacion.html',
            context_dict
            )

@staff_member_required(login_url='votos:login')
def edit_poll(request, poll_id):
    poll = get_object_or_404(models.Poll, pk=poll_id)

    if request.method == 'POST':
        form = forms.EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, 'Votacion actualizada correctamente',
                             extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse('votos:list'))

    form = forms.EditPollForm(instance=poll)

    return render(request, "votos/editar_votacion.html", {'form': form, 'poll': poll})


@staff_member_required(login_url='votos:login')
def delete_poll(request, poll_id):
    poll = get_object_or_404(models.Poll, pk=poll_id)
    poll.delete()
    messages.success(request, 'Votacion eliminada correctamente',
                     extra_tags='alert alert-success alert-dismissible fade show')
    return HttpResponseRedirect(reverse('votos:list'))

@staff_member_required(login_url='votos:login')
def add_choice(request, poll_id):
    poll = get_object_or_404(models.Poll, pk=poll_id)

    if request.method == 'POST':
        form = forms.AddChoiceForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Eleccion agregada correctamente", extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse('votos:edit', args=[poll.id]))
    else:
        form = forms.AddChoiceForm()
    context = {
        'form': form,
    }
    return render(request, 'votos/agregar_eleccion.html', context)

@staff_member_required(login_url='votos:login')
def edit_choice(request, choice_id):
    choice = get_object_or_404(models.Choice, pk=choice_id)
    poll = get_object_or_404(models.Poll, pk=choice.poll.id)
    
    if request.method == 'POST':
        form = forms.AddChoiceForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Eleccion actualizada exitosamente", extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse('votos:edit', args=[poll.id]))
    else:
        form = forms.AddChoiceForm(instance=choice)
    context = {
        'form': form,
        'editChoice': True,
        'choice': choice,
    }
    return render(request, 'votos/agregar_eleccion.html', context)

@staff_member_required(login_url='votos:login')
def delete_choice(request, choice_id):
    choice = get_object_or_404(models.Choice, pk=choice_id)
    poll = get_object_or_404(models.Poll, pk=choice.poll.id)
    choice.delete()
    messages.success(
        request, "Eleccion eliminada exitosamente", extra_tags='alert alert-success alert-dismissible fade show')
    return HttpResponseRedirect(reverse('votos:edit', args=[poll.id]))

def result_poll(request, poll_id):
    poll = get_object_or_404(models.Poll, id=poll_id)
    
    return render(request, 'votos/resultado_votacion.html', {'poll': poll})

def detail_poll(request, poll_id):
    poll = get_object_or_404(models.Poll, id=poll_id)
    if not poll.active:
        return render(request, 'votos/resultado_votacion.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loopTime': range(0, loop_count),
    }
    return render(request, 'votos/detalle_votacion.html', context)

@login_required
def vote_poll(request, poll_id):
    poll = get_object_or_404(models.Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    
    if not poll.user_can_vote(request.user):
        messages.error(
            request, "Ya has votado!", extra_tags='alert alert-warning alert-dismissible fade show')
        return HttpResponseRedirect(reverse('votos:list'))

    if choice_id:
        choice = models.Choice.objects.get(id=choice_id)
        vote = models.Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        
        return render(request, 'votos/resultado_votacion.html', {'poll': poll})
    else:
        messages.error(
            request, "No has seleccionado una opcion", extra_tags='alert alert-warning alert-dismissible fade show')
        return HttpResponseRedirect(reverse('votos:detail', args=[poll.id,]))
    
    return render(request, 'polls/poll_result.html', {'poll': poll})


@staff_member_required(login_url='votos:login')
def end_poll(request, poll_id):
    poll = get_object_or_404(models.Poll, pk=poll_id)
    
    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'votos/resultado_votacion.html', {'poll': poll})
    else:
        return render(request, 'votos/resultado_votacion.html', {'poll': poll})
