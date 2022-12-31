from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]