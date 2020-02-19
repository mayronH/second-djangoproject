from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
# from django.template import loader
from .models import Question, Choice
# Create your views here.


# Carregamndo um template e passando um context
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#       'latest_question_list' : latest_question_list,
#     }
#     return HttpResponse(template.render(context,request))

#Utilizando um atalho render, eliminando o loader e o HttpResponse
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

#Código mais limpo
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})

#Mostrando um objeto ou mostrando uma página 404 caso não encontrado
# def detail(request,question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question':question})

#Mesmo código mas utilizando um atalho
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question':question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Try catch verifica se a opção escolhida existe
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Se não existir retorna para a votação
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "Você não escolheu uma opção.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Para previnir que usuário envie o mesmo formulário clicando no botão de voltar a página
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  

#Como index, detail e result têm o mesmo código, melhor utilizar views genéricas:

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Filtra os objetos que possuem a data de publicação anterior ou igual a data atual
        return Question.objects.filter(pub_date__lte=timezone.now()).filter(choice__isnull=False).distinct().order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'





