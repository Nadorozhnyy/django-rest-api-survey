# Generated by Django 4.1.2 on 2023-01-26 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='survey name')),
                ('start_date', models.DateTimeField(db_index=True, verbose_name='survey start date')),
                ('end_date', models.DateTimeField(db_index=True, verbose_name='survey end date')),
                ('description', models.TextField(max_length=2500, verbose_name='survey description')),
            ],
            options={
                'verbose_name': 'survey',
                'verbose_name_plural': 'surveys',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=2500, verbose_name='text answer')),
                ('question_type', models.CharField(choices=[('TEXT_ANSWER', 'text answer'), ('ONE_CHOICES_ANSWER', 'single choice answer'), ('MULTI_CHOICES_ANSWER', 'multiple choice answer')], max_length=250, verbose_name='question type')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='app_survey.survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=250, verbose_name='possible answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_choice', to='app_survey.surveyquestion', verbose_name='question')),
            ],
            options={
                'verbose_name': 'possible answer',
                'verbose_name_plural': 'possible answers',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='id')),
                ('choice_text', models.TextField(blank=True, max_length=250, null=True, verbose_name='text answer')),
                ('choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_choice', to='app_survey.questionchoice', verbose_name='single choice answer')),
                ('choices', models.ManyToManyField(blank=True, related_name='answer_choices', to='app_survey.questionchoice', verbose_name='multiple choice answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_question', to='app_survey.surveyquestion', verbose_name='question')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_survey', to='app_survey.survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
                'ordering': ['id'],
            },
        ),
    ]