"""Views for the multilingual_survey app."""
from django.views.generic import DetailView, FormView, ListView
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status, viewsets
from django.forms.models import model_to_dict

from django.contrib.auth.models import User
from . import forms
from . import models

from .serializers import SurveySerializer, SurveyDetailSerializer, SurveyQuestionSerializer, UserSerializer, SurveyAnswerSerializer, SurveyResponseSerializer


class SurveyReportAdminView(DetailView):
    """A view to display results of a survey for admins."""
    model = models.Survey
    template_name = 'multilingual_survey/survey_report_admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('answer'):
            try:
                self.answer = models.SurveyAnswer.objects.get(
                    pk=request.GET['answer'])
            except models.SurveyAnswer.DoesNotExist:
                pass
        return super(SurveyReportAdminView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SurveyReportAdminView, self).get_context_data(**kwargs)
        if hasattr(self, 'answer') and self.answer:
            context.update({
                'user_selection': self.answer.responses.values_list(
                    'user__pk', flat=True),
                'session_selection': self.answer.responses.values_list(
                    'session_id', flat=True),
                'current_answer': self.answer,
            })
        return context


class SurveyReportListView(ListView):
    """A view to display a list of surveys for admins."""
    model = models.Survey
    template_name = 'multilingual_survey/survey_report_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(SurveyReportListView, self).dispatch(
            request, *args, **kwargs)


class SurveyView(FormView):
    """A view to display a survey."""
    form_class = forms.SurveyForm
    template_name = 'multilingual_survey/survey_detail.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.survey = models.Survey.objects.get(slug=kwargs['slug'])
        except models.Survey.DoesNotExist:
            raise Http404
        return super(SurveyView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SurveyView, self).get_context_data(**kwargs)
        context.update({'survey': self.survey})
        return context

    def get_form_kwargs(self):
        kwargs = super(SurveyView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'survey': self.survey,
            'session_key': self.request.session.session_key,
        })
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context.update({'success': True})
        return self.render_to_response(context)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class SurveyList(APIView):
    """
    List all surveys, or create a new survey.
    """
    def get(self, request, format=None):
        user_language = request.GET.get('language')
        queryset = models.Survey.objects.language(user_language).all()
        serializer = SurveySerializer(queryset, many=True)
        return JSONResponse(serializer.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = SurveySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyDetail(APIView):
    """
    Retrieve, update or delete a survey instance.
    """
    def get_object(self, pk):
        try:
            user_language = self.request.GET.get('language')
            return models.Survey.objects.language(user_language).get(pk=pk)
        except models.Survey.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get_related_questions(self, pk):
        try:
            user_language = self.request.GET.get('language')
            return models.SurveyQuestion.objects.language(user_language).all().filter(survey=pk)
        except models.SurveyAnswer.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get_related_answers(self, pk):
        try:
            user_language = self.request.GET.get('language')
            return models.SurveyAnswer.objects.language(user_language).all().filter(question=pk)
        except models.SurveyAnswer.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        survey = self.get_object(pk)
        serializer = SurveyDetailSerializer(survey)
        return JSONResponse(serializer.data)

    def put(self, request, pk, format=None):
        survey = self.get_object(pk)
        serializer = SurveyDetailSerializer(survey, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        survey = self.get_object(pk)
        survey.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class QuestionList(APIView):
    """
    List all questions, or create a new question.
    """
    def get(self, request, format=None):
        user_language = request.GET.get('language')
        queryset = models.SurveyQuestion.objects.language(user_language).all()
        serializer = SurveyQuestionSerializer(queryset, many=True)
        return JSONResponse(serializer.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = SurveyQuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyResponseList(APIView):
    def get(self, request, format=None):
        queryset = models.SurveyResponse.objects.all()
        serializer = SurveyResponseSerializer(queryset, many=True, context={'request': request})
        return JSONResponse(serializer.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = SurveyResponseSerializer(data=data, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyResponseSummary(APIView):
    def list_to_dict(self, vals):
        x = {}
        for k, v in vals:
            x.setdefault(k, []).append(v)
        return x

    def dict_avg(self, d):
        x = {}
        for k, v in d.iteritems():
            x[k] = sum([int(vp) for vp in v])/len(v)
        return x

    def get(self, request, pk, format=None):
        output = request.query_params.get("output")
        if output == 'average':
            queryset = models.SurveyResponse.objects.filter(question__survey_id=pk).values_list('question_id','other_answer_numeric')
            set_as_dict = self.list_to_dict(queryset)
            averages = self.dict_avg(set_as_dict)
            return JSONResponse(averages)
        elif output == 'values':
            queryset = models.SurveyResponse.objects.filter(question__survey_id=pk).values_list('question_id','other_answer_numeric')
            set_as_dict = self.list_to_dict(queryset)
            return JSONResponse(set_as_dict)
        else:
            queryset = models.SurveyResponse.objects.filter(question__survey_id=pk)
            serializer = SurveyResponseSerializer(queryset, many=True)
            return JSONResponse(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer