from django.db.models import F
from django.shortcuts import render, get_object_or_404, get_list_or_404 
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone   
from .models import Question, Choice
from django.views import generic

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    pk_url_kwarg = "question_id"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    pk_url_kwarg = "question_id"

def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        choice_pk = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_pk)
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, "polls/detail.html", context) 
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))