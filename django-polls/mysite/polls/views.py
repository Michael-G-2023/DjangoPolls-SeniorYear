from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


from .models import Choice, Question, Response

class DetailView(generic.DetailView):
    model = Question
    
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request,args,kwargs)
        taken_users = User.objects.filter(response__choice__question = pk)
        if request.user in taken_users:
            return response
        else:
            return HttpResponseRedirect(reverse('polls:detail', args))



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
def results(request, pk):
    taken_users = User.objects.filter(response__choice__question = pk)
    if request.user in taken_users:
        question = Question.objects.get(pk=pk)
        return render(request, 'polls/results.html', {'question': question})
    else:
        return HttpResponseRedirect(reverse('polls:detail', args = pk))

def detail(request, question_id):
    #currentuser = Question.objects.filter(choice__response__user = request.user)
    usersvoted = User.objects.filter(response__choice__question = question_id)
    question = Question.objects.get(pk=question_id)

    if request.user in usersvoted:
        return render(request, 'polls/results.html', {'question': question})    
    #question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def index(request):
    pollsresponded = Question.objects.filter(choice__response__user = request.user)
    noresponse = Question.objects.filter(choice__repsonse__user = request.user)
    return render

def vote(request, question_id):
    #taken_users = User.objects.filter(response__choice__question = question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        response = Response(user = request.user, dayandtime = datetime.datetime.now(), choice = selected_choice)
        #if response in taken_users:
            #taken_users.delete(response)
        response.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
