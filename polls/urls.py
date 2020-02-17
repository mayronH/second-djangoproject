from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('<int:pk>/', views.DetailView, name='detail'),
    path('<int:pk>/results/', views.ResultsView, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
