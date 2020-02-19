import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

    #A versão de cima não verifica se a data de publicação está no futuro, a de baixo sim:
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    #Modifica as informações na tabela no admin
    #Ordenar pela data de publicação
    was_published_recently.admin_order_field ='pub_date'
    #Modifica o texto 'False' 'True' por um ícone visual
    was_published_recently.boolean = True
    #Modifica o cabeçalho da coluna
    was_published_recently.short_description = 'Published recently?'


    def __str__(self):
        return self.question_text

    def votes_total(self):
        count = 0
        for choice in self.choice_set.all():
            count += choice.votes 
        return count


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage_votes(self):
        total = self.question.votes_total()
        porcentagem = (self.votes/total)
        return format(porcentagem, ".0%")

    def __str__(self):
        return self.choice_text