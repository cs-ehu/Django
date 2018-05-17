"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.http import JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    themes = list(set([obj.theme for obj in latest_question_list]))
    template = loader.get_template('polls/index.html')
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
                'themes': themes,
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,)))

def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form})

def choice_add(request, question_id):
        question = Question.objects.get(id = question_id)
        if request.method =='POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():
                choice = form.save(commit = False)
                choice.question = question
                choice.vote = 0
                choice.save()         
                #form.save()
        else: 
            form = ChoiceForm()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text,'form': form})

def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)

def theme_q(request, question_theme):
    q=Question.objects.filter(theme = question_theme)
    template = loader.get_template('polls/theme_q.html')
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': q,
                'theme': question_theme,
              }
    return render(request, 'polls/theme_q.html', context)

def tema(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    themes = list(set([obj.theme for obj in latest_question_list]))
    template = loader.get_template('game/tema.html')
    context = {
                'title':'Lista de temas',
                'themes': themes,
              }
    return render(request, 'game/tema.html', context)

def game(request, theme):
    q=Question.objects.filter(theme = theme)
    template = loader.get_template('game/game.html')
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': q,
                'theme': theme,
              }
    return render(request, 'game/game.html', context)

def pregunta(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'game/pregunta.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def respuesta(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
                'title':'Resultados de la pregunta:',
                'question' : question,
        }
    return render(request, 'game/respuesta.html', context)

def validate_question(request):
    q = get_object_or_404(Question, pk=request.GET.get('question',None))
    correct_answer = Choice.objects.filter(question=q).get(correct=True)
    try:
        selected_choice = Choice.objects.get(pk=request.GET.get('answer',None))
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': q.id,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        if correct_answer.id==selected_choice.id:
            data = {
                    'response' : 'correct'
                }
        else:
            data  = {
                    'response' : 'incorrect',
                    'correct': correct_answer.id
                }
        return JsonResponse(data)
