from django.db import models

TEXT_ANSWER = 'TEXT_ANSWER'
ONE_CHOICES_ANSWER = 'ONE_CHOICES_ANSWER'
MULTI_CHOICES_ANSWER = 'MULTI_CHOICES_ANSWER'


class Survey(models.Model):
    name = models.CharField(max_length=256, verbose_name='survey name')
    start_date = models.DateTimeField(db_index=True, verbose_name='survey start date')
    end_date = models.DateTimeField(db_index=True, verbose_name='survey end date')
    description = models.TextField(max_length=2500, verbose_name='survey description')

    class Meta:
        ordering = ['id']
        verbose_name = 'survey'
        verbose_name_plural = 'surveys'

    def __str__(self):
        return self.name


class SurveyQuestion(models.Model):
    QUESTION_TYPE = (
        (TEXT_ANSWER, 'text answer'),
        (ONE_CHOICES_ANSWER, 'single choice answer'),
        (MULTI_CHOICES_ANSWER, 'multiple choice answer'),
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='question', verbose_name='survey')
    question_text = models.TextField(max_length=2500, verbose_name='text answer')
    question_type = models.CharField(max_length=250, choices=QUESTION_TYPE, verbose_name='question type')

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'

    def __str__(self):
        return f'{self.question_text}_{self.get_question_type_display()}'


class QuestionChoice(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='question_choice',
                                 verbose_name='question')
    choice_text = models.CharField(max_length=250, verbose_name='possible answer')

    class Meta:
        verbose_name = 'possible answer'
        verbose_name_plural = 'possible answers'

    def __str__(self):
        return f'{self.question.survey.id}_{self.question.id}: {self.choice_text}'


class Answer(models.Model):
    user_id = models.IntegerField(verbose_name='id')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='answer_survey', verbose_name='survey')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='answer_question',
                                 verbose_name='question')
    choice_text = models.TextField(max_length=250, null=True, blank=True, verbose_name='text answer')
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='answer_choice', verbose_name='single choice answer')
    choices = models.ManyToManyField(QuestionChoice, blank=True, related_name='answer_choices',
                                     verbose_name='multiple choice answer')

    class Meta:
        ordering = ['id']
        verbose_name = 'answer'
        verbose_name_plural = 'answers'

    def __str__(self):
        return f'{self.user_id}_{self.survey}'



