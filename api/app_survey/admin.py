from django.contrib import admin
from .models import Survey, SurveyQuestion, QuestionChoice, Answer


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'description')


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'question_text', 'question_type')


@admin.register(QuestionChoice)
class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choice_text')


@admin.register(Answer)
class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'survey', 'question', 'choice_text', 'choice')
    filter_horizontal = ('choices',)
