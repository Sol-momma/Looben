from multiprocessing import connection
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.db.models import Q # 検索機能のために追加

from .forms import QuestionForm, AnswerForQuestionForm
from .models import Questions, AnswerForQuestion


class QuestionView(ListView):
    template_name = 'question/question.html'
    model = Questions
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 回答募集中の質問を4つ取得
        question_seeking_answers = Questions.objects.filter(is_solved=False).all()[:4]
        context['question_seeking_answers'] = question_seeking_answers    
        # 最新の解決済みの質問を4つ取得  
        solved_questions = Questions.objects.filter(is_solved=True).all()[:4]
        context['solved_questions'] = solved_questions
        return context
    
    
@login_required
def ask_question(request):
    ask_question_form = QuestionForm(request.POST or None)
    if ask_question_form.is_valid():
        ask_question_form.instance.user = request.user
        ask_question_form.save()
        return redirect('questions:question')
    return render(
        request, 'question/ask_question.html', context={
            'ask_question_form': ask_question_form
        }
    )
    
    
class QuestionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'question/question_detail.html'
    model = Questions
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 質問に対する回答の数
        number_of_answer = self.object.answerforquestion_set.all().count()
        context['number_of_answer'] = number_of_answer
        context['form'] = AnswerForQuestionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AnswerForQuestionForm(request.POST or None)
        if form.is_valid():
            form.instance.question = self.object.id
            form.instance.user = request.user
            form.save()
            return redirect('question:question_detail', pk=self.object.id)
        else:
            context = self.get_context_data()
            context['form'] = form  # form.is_validしたフォームを渡さないと、フォームのエラーを表示できない
            return render(request, 'question:question_detail', context)
    
    
class CategorizedQuestionsView(DetailView):
    model = Questions
    template_name = 'question/categorized_questions.html'
    
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'category'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        # 選択されたカテゴリーの質問を取得
        context['categorized_questions'] = Questions.objects.filter(category=self.object.category)
        # 質問に対する回答の数
        number_of_answer = self.object.answerforquestion_set.all().count()
        context['number_of_answer'] = number_of_answer
        return context

