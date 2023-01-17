from django.db import models

TEXT_ANSWER = 'TEXT_ANSWER'
ONE_CHOICES_ANSWER = 'ONE_CHOICES_ANSWER'
MULTI_CHOICES_ANSWER = 'MULTI_CHOICES_ANSWER'


class Survey(models.Model):
    name = models.CharField(max_length=256, verbose_name='название опроса')
    start_date = models.DateTimeField(db_index=True, verbose_name='дата старта опроса')
    end_date = models.DateTimeField(db_index=True, verbose_name='дата окончания опроса')
    description = models.TextField(max_length=2500, verbose_name='описание опроса')

    class Meta:
        ordering = ['id']
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'

    def __str__(self):
        return self.name


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='question', verbose_name='опрос')
    question_text = models.TextField(max_length=2500, verbose_name='текст вопроса')
    QUESTION_TYPE = (
        (TEXT_ANSWER, 'ответ текстом'),
        (ONE_CHOICES_ANSWER, 'ответ с выбором одного варианта'),
        (MULTI_CHOICES_ANSWER, 'ответ с выбором нескольких вариантов'),
    )
    question_type = models.CharField(max_length=250, choices=QUESTION_TYPE, verbose_name='тип вопроса')

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return f'{self.question_text}_{self.get_question_type_display()}'


class QuestionChoice(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='question_choice',
                                 verbose_name='вопрос')
    choice_text = models.CharField(max_length=250, verbose_name='вариант ответа')

    class Meta:
        verbose_name = 'вариант ответа'
        verbose_name_plural = 'варианты ответа'

    def __str__(self):
        return f'{self.question.survey.id}_{self.question.id}: {self.choice_text}'


class Answer(models.Model):
    user_id = models.IntegerField(verbose_name='ид')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='answer_survey', verbose_name='опрос')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='answer_question',
                                 verbose_name='вопрос')
    choice_text = models.TextField(max_length=250, null=True, blank=True, verbose_name='ответ текстом')
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='answer_choice', verbose_name='ответ с выбором одного варианта')
    choices = models.ManyToManyField(QuestionChoice, blank=True, related_name='answer_choices',
                                     verbose_name='ответ с выбором нескольких вариантов')

    class Meta:
        ordering = ['id']
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return f'{self.user_id}_{self.survey}'



