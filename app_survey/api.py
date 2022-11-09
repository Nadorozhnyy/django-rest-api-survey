from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import Survey, SurveyQuestion, QuestionChoice
from .serializers import SurveySerializer, SurveyQuestionSerializer, QuestionChoiceSerializer
from .permissions import IsAdminOrReadOnly


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.get_queryset().order_by('id')
    serializer_class = SurveySerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(methods=['get'], detail=True, permission_classes=[IsAdminOrReadOnly], url_path='questions',
            url_name='questions')
    def questions(self, request, pk=None):
        instance = self.get_object()
        today = timezone.now()
        if not instance.start_date <= today <= instance.end_date and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'questions list not available'})
        questions = SurveyQuestion.objects.filter(survey=pk)
        serializer = SurveyQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        #TODO рефактор фильтра
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            today = timezone.now()
            queryset = self.filter_queryset(self.get_queryset()).filter(end_date__gte=today).filter(
                start_date__lte=today)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        today = timezone.now()
        if not instance.start_date <= today <= instance.end_date and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'survey not available'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.get_queryset().order_by('id')
    serializer_class = SurveyQuestionSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(methods=['get'], detail=True, permission_classes=[IsAdminOrReadOnly], url_path='choices',
            url_name='choices')
    def choices(self, request, pk=None):
        instance = self.get_object()
        today = timezone.now()
        if not instance.survey.start_date <= today <= instance.survey.end_date and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'choices list not available'})
        choices = QuestionChoice.objects.filter(question=pk)
        serializer = QuestionChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            today = timezone.now()
            queryset = self.filter_queryset(self.get_queryset()).filter(survey__end_date__gte=today).filter(
                survey__start_date__lte=today)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        today = timezone.now()
        if not instance.survey.start_date <= today <= instance.survey.end_date and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'question not available'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class QuestionChoiceViewSet(viewsets.ModelViewSet):
    queryset = QuestionChoice.objects.get_queryset().order_by('id')
    serializer_class = QuestionChoiceSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            today = timezone.now()
            queryset = self.filter_queryset(self.get_queryset()).filter(question__survey__end_date__gte=today).filter(
                question__survey__start_date__lte=today)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        today = timezone.now()
        if not instance.question.survey.start_date <= today <= instance.question.survey.end_date \
                and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'choices not available'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
