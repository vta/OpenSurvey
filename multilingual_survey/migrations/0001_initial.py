# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-11 01:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_libs.models_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=256, unique=True, verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
            bases=(django_libs.models_mixins.TranslationModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=256, verbose_name='Slug')),
            ],
            bases=(django_libs.models_mixins.TranslationModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SurveyAnswerTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='multilingual_survey.SurveyAnswer')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'multilingual_survey_surveyanswer_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=256, verbose_name=b'Slug')),
                ('is_multi_select', models.BooleanField(default=False, verbose_name='Is multi-select')),
                ('type', models.CharField(choices=[(b'0', b'text'), (b'1', b'checkbox'), (b'2', b'radio'), (b'3', b'range'), (b'4', b'dropdown'), (b'5', b'zipcode'), (b'6', b'email')], default=b'0', max_length=1)),
                ('scale_min', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('scale_max', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('has_other_field', models.BooleanField(default=False, verbose_name='Has other-field')),
                ('required', models.BooleanField(default=False, verbose_name='Required')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='multilingual_survey.Survey', verbose_name='Survey')),
            ],
            bases=(django_libs.models_mixins.TranslationModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SurveyQuestionTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='multilingual_survey.SurveyQuestion')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'multilingual_survey_surveyquestion_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, max_length=1024, verbose_name='Session ID')),
                ('other_answer_numeric', models.IntegerField(blank=True, null=True, verbose_name='Other answer numeric')),
                ('other_answer', models.CharField(blank=True, max_length=1024, verbose_name='Other answer')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='multilingual_survey.SurveyAnswer', verbose_name='Answer')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='multilingual_survey.SurveyQuestion', verbose_name='Question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ('question',),
            },
        ),
        migrations.CreateModel(
            name='SurveyTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=2048, verbose_name='Description')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='multilingual_survey.Survey')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'multilingual_survey_survey_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='multilingual_survey.SurveyQuestion', verbose_name='Question'),
        ),
        migrations.AlterUniqueTogether(
            name='surveytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='surveyquestiontranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='surveyquestion',
            unique_together=set([('slug', 'survey')]),
        ),
        migrations.AlterUniqueTogether(
            name='surveyanswertranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='surveyanswer',
            unique_together=set([('slug', 'question')]),
        ),
    ]
