from rest_framework import serializers
from django.utils import timezone

from .models import Survey, SurveyQuestion, QuestionChoice


class SurveySerializer(serializers.ModelSerializer):
    #TODO понять что это
    survey = serializers.StringRelatedField(many=True)

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
        if start_date < today:
            raise serializers.ValidationError({f'start_date': f'start_date cannot be earlier than the {today.date()}'})

    def create(self, validated_data):
        start_date = validated_data['start_date']
        self.start_date_validator(start_date)
        self.date_survey_validator(validated_data, start_date)
        return Survey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('start_date', None)
        super().update(instance, validated_data)
        start_date = instance.start_date
        self.date_survey_validator(validated_data, start_date)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class SurveyQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyQuestion
        fields = '__all__'


class QuestionChoiceSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        question = validated_data['question']
        if question.type == 0:
            raise serializers.ValidationError({f'choices': 'cannot create choices for question with text answer'})
        return Survey.objects.create(**validated_data)

    class Meta:
        model = QuestionChoice
        fields = '__all__'
