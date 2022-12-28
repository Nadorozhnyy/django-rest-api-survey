from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from .models import Survey, SurveyQuestion, QuestionChoice, Answer, TEXT_ANSWER, ONE_CHOICES_ANSWER, \
    MULTI_CHOICES_ANSWER


class AnswerSerializer(serializers.ModelSerializer):

    @staticmethod
    def question_type_match_answer_validate(choice_text, choice, choices, question):
        if question.question_type == TEXT_ANSWER and bool(choice_text) is True:
            pass
        elif question.question_type == ONE_CHOICES_ANSWER and bool(choice) is True:
            pass
        elif question.question_type == MULTI_CHOICES_ANSWER and bool(choices) is True:
            pass
        else:
            raise serializers.ValidationError({f'answers': 'question type must match the answer type'})

    @staticmethod
    def answer_count_zero_or_one(choice_text, choice, choices):
        if [bool(choice_text), bool(choice), bool(choices)].count(True) > 1:
            raise serializers.ValidationError({f'answers': 'it can be one or zero type of answers'})

    @staticmethod
    def answer_belongs_to_question(validate_data):
        question = validate_data['question']
        answer = ''
        if validate_data['choice']:
            answer = [validate_data['choice']]
        elif validate_data['choices']:
            answer = validate_data['choices']
        choices_list = QuestionChoice.objects.filter(question=question)
        if not set(answer).issubset(choices_list):
            raise serializers.ValidationError({f'answers': 'answer not related with question'})

    def validate(self, attrs):
        choice = attrs['choice']
        choice_text = attrs['choice_text']
        choices = attrs['choices']
        question = attrs['question']
        self.answer_count_zero_or_one(choice_text, choice, choices)
        self.question_type_match_answer_validate(choice_text, choice, choices, question)
        self.answer_belongs_to_question(attrs)
        return attrs

    class Meta:
        model = Answer
        fields = ('id', 'question', 'choice', 'choice_text', 'choices')
        read_only_fields = ('id',)


class QuestionChoiceSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        question = validated_data['question']
        if question.question_type == TEXT_ANSWER:
            raise serializers.ValidationError({f'choices': 'cannot create choices for question with text answer'})
        return QuestionChoice.objects.create(**validated_data)

    class Meta:
        model = QuestionChoice
        fields = '__all__'


class SurveyQuestionSerializer(serializers.ModelSerializer):
    question_choice = QuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = SurveyQuestion
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = '__all__'

    @staticmethod
    def date_survey_validator(validated_data, start_date):
        if 'end_date' in validated_data:
            end_date = validated_data['end_date']
            if start_date > end_date:
                raise serializers.ValidationError({'end_date': 'end_date cannot be earlier than the start_date '})

    @staticmethod
    def start_date_validator(start_date):
        today = timezone.now()
        if start_date.date() < today.date():
            raise serializers.ValidationError({f'start_date': f'start_date cannot be earlier than the {today.date()}'})

    def validate(self, attrs):
        start_date = attrs['start_date']
        self.start_date_validator(start_date)
        self.date_survey_validator(attrs, start_date)
        return attrs

    def update(self, instance, validated_data):
        if instance.start_date != validated_data['start_date']:
            raise serializers.ValidationError({f'start_date': f'cannot change start date'})
        start_date = instance.start_date
        self.date_survey_validator(validated_data, start_date)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PassedSurveySerializer(serializers.ModelSerializer):
    answer_survey = serializers.SerializerMethodField('get_users_answer')

    def get_users_answer(self, survey):
        user_id = self.context['request'].user.id
        user_id_param = self.context['request'].query_params.get('user_id')
        if self.context['request'].user.is_staff:
            if user_id_param:
                answers_queryset = Answer.objects.all().filter(Q(survey=survey), user_id=user_id_param).select_related()
            else:
                answers_queryset = Answer.objects.all().filter(Q(survey=survey)).select_related()
        else:
            answers_queryset = Answer.objects.all().filter(Q(survey=survey), user_id=user_id).select_related()
        serializer = AnswerSerializer(instance=answers_queryset, many=True, read_only=True, context=self.context)
        return serializer.data

    class Meta:
        model = Survey
        fields = ['id', 'name', 'answer_survey']
