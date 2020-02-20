from django.contrib import admin
from .models import Question,Choice

# Register your models here.

#Modelo do formulário, a ordem faz diferença
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

#Dividindo campos em grupos
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,                  {'fields':['question_text']}),
#         ('Date information',    {'fields': ['pub_date']}),
#     ]

#Cria o formulário com 2 choices um embaixo do outro
# class ChoiceInLine(admin.StackedInline):
#     model = Choice
#     extra = 2

#Cria o formulário em forma de tabela, mais compacto
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2

#Colocando o formulário de choices dentro de question
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        # Collapse do grupo inteiro
        ('Date information',    {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInLine]

    #Edita a tabela dos objetos, é possível incluir métodos tbm
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    #Cria um filtro por data
    list_filter = ['pub_date']
    #Cria um input de pesquisa, a pesquisa é feita só no question_text
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

#Esses são os formulários padrões
# admin.site.register(Question)
# admin.site.register(Choice)
