from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=256, verbose_name='название опроса')
    start_date = models.DateTimeField(verbose_name='дата старта опроса')
    end_date = models.DateTimeField(verbose_name='дата окончания опроса')
    description = models.TextField(max_length=2500, verbose_name='описание опроса')

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'

    def __str__(self):
        return self.name


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey', verbose_name='опрос')
    question_text = models.TextField(max_length=2500, verbose_name='текст вопроса')
    QUESTION_TYPE_CHOICES = (
        (0, 'ответ текстом'),
        (1, 'ответ с выбором одного варианта'),
        (2, 'ответ с выбором нескольких вариантов'),
    )
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPE_CHOICES, verbose_name='тип вопроса')

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return str(self.question_text) + '_' + str(self.QUESTION_TYPE_CHOICES[int(self.question_type)][1])


class QuestionChoice(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='question_choice',
                                 verbose_name='вопрос')
    choice_text = models.CharField(max_length=250, null=True, verbose_name='вариант ответа')

    class Meta:
        verbose_name = 'вариант ответа'
        verbose_name_plural = 'варианты ответа'

    def __str__(self):
        return str(self.question) + '_' + str(self.id)



