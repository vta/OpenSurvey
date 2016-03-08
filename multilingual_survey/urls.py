"""URLs for the multilingual_survey app."""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # url(r'^report/(?P<slug>[\w-]+)/$',
    #     views.SurveyReportAdminView.as_view(),
    #     name='multilingual_survey_admin_report'),
    # url(r'^report/$',
    #     views.SurveyReportListView.as_view(),
    #     name='multilingual_survey_list_report'),
    # url(r'^(?P<slug>[\w-]+)/$',
    #     views.SurveyView.as_view(),
    #     name='multilingual_survey_detail'),

    url(r'^', include(router.urls)),

    url(r'^surveys/$', views.SurveyList.as_view()),
    url(r'^surveys/(?P<pk>[0-9]+)/$', views.SurveyDetail.as_view()),

    url(r'^responses/$', views.SurveyResponseList.as_view()),

    url(r'^questions/$', views.QuestionList.as_view()),
]
