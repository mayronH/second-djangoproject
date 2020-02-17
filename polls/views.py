from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
# from django.template import loader
from .models import Question
# Create your views here.


# Carregamndo um template e passando um context
# def index(request):
#     lastest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#       'lastest_question_list' : lastest_question_list,
#     }
#     return HttpResponse(template.render(context,request))

#Utilizando um atalho render, eliminando o loader e o HttpResponse
# def index(request):
#     lastest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'lastest_question_list' : lastest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

#Código mais limpo
def index(request):
    lastest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'lastest_question_list': lastest_question_list})

#Mostrando um objeto ou mostrando uma página 404 caso não encontrado
# def detail(request,question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question':question})

#Mesmo código mas utilizando um atalho
def detail(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    return HttpResponse("Resultados da questão %s." % question_id)

def vote(request,question_id):
    return HttpResponse("Votação: %s." % question_id)


