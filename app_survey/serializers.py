from rest_framework import serializers
from .models import Survey, SurveyQuestion, QuestionChoice


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

    @staticmethod
    def date_survey_validator(validated_data):
        if 'start_date' and 'end_date' in validated_data:
            start_date = validated_data['start_date']
            end_date = validated_data['end_date']
            if start_date > end_date:
                raise serializers.ValidationError({'end_date': 'end_date cannot be earlier than the start_date '})

    def create(self, validated_data):
        self.date_survey_validator(validated_data)
        return Survey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'start_date' in validated_data:
            raise serializers.ValidationError({'start_date': 'you cannot change the start_date field'})
        self.date_survey_validator(validated_data)
        instance.save()
        return instance


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = '__all__'


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = '__all__'
