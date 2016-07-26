from hvad.contrib.restframework import TranslatableModelSerializer, HyperlinkedTranslatableModelSerializer
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User

from . import models


class SurveyAnswerSerializer(TranslatableModelSerializer):
    position = serializers.SerializerMethodField()

    def get_position(self, obj):
        return obj.generic_position.get().position


    class Meta:
        model = models.SurveyAnswer
        fields = ['pk', 'title', 'subtitle', 'slug', 'question', 'meta_integer', 'position']

class SurveyQuestionSerializer(TranslatableModelSerializer):
    answers = SurveyAnswerSerializer(many=True)
    type = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    def get_position(self, obj):
        return obj.generic_position.get().position

    def get_type(self, obj):
        return models.QUESTION_TYPE_CHOICES[int(obj.type)][1]

    class Meta:
        model = models.SurveyQuestion
        fields = ['pk', 'title', 'content', 'slug', 'survey', 'is_multi_select', 'position', 'type', 'scale_min','scale_max', 'has_other_field', 'required', 'answers']

class SurveyDetailSerializer(TranslatableModelSerializer):
    questions = SurveyQuestionSerializer(many=True)

    class Meta:
        model = models.Survey
        fields = ['pk', 'title', 'description', 'slug', 'questions']

class SurveySerializer(TranslatableModelSerializer):

    class Meta:
        model = models.Survey
        fields = ['pk', 'title', 'description', 'slug']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class SurveyResponseSerializer(serializers.HyperlinkedModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=models.SurveyQuestion.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=models.SurveyAnswer.objects.all())

    class Meta:
        model = models.SurveyResponse
        fields = ( 'ip_address', 'session_id', 'question', 'answer', 'other_answer', 'other_answer_numeric', 'date_created')