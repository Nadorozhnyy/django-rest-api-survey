from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from .models import Survey, SurveyQuestion, QuestionChoice, Answer
from .serializers import SurveySerializer, SurveyQuestionSerializer, QuestionChoiceSerializer, AnswerSerializer, \
    PassedSurveySerializer
from .permissions import IsAdminOrReadOnly


class ObjectViewSet(viewsets.ModelViewSet):
    """
    Base class for Survey, Question and Question choices
    """
    url_path = None
    url_name = None
    model = None
    model_serializer = None

    def get_queryset_with_filter(self):
        """
        Filtered queryset for not staff user (showing actual survey and questions)
        :return: QuerySet
        """
        pass

    @staticmethod
    def check_date(request, instance):
        """
        Raise AuthenticationFailed if date not actual for users
        :param request: request
        :param instance: models.Survey
        """
        pass

    def get_instance_objects(self, pk):
        """
        Pk instance of relevant object
        :param pk: int
        :return: Queryset
        """
        pass

    def action_object(self, request, pk=None):
        """
        Action to view object with detail
        :param request: request
        :param pk: int
        :return: Response
        """
        instance = self.get_object()
        self.check_date(request, instance)
        instance_object = self.get_instance_objects(pk)
        serializer = self.model_serializer(instance_object, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.get_queryset_with_filter()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_date(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SurveyViewSet(ObjectViewSet):
    queryset = Survey.objects.order_by('id')
    serializer_class = SurveySerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)

    url_path = 'questions'
    url_name = 'questions'
    model = SurveyQuestion
    model_serializer = SurveyQuestionSerializer

    def get_queryset_with_filter(self):
        today = timezone.now()
        return self.filter_queryset(self.get_queryset()).filter(end_date__gte=today).filter(
                start_date__lte=today)

    @staticmethod
    def check_date(request, instance):
        today = timezone.now()
        if not instance.start_date <= today <= instance.end_date and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'object not available'})

    def get_instance_objects(self, pk):
        return self.model.objects.filter(survey=pk)

    @action(methods=['get'], detail=True, permission_classes=[IsAdminOrReadOnly, IsAuthenticated], url_path=url_path,
            url_name=url_name)
    def action_object(self, request, pk=None):
        return super().action_object(request, pk)


class SurveyQuestionViewSet(ObjectViewSet):
    queryset = SurveyQuestion.objects.order_by('id')
    serializer_class = SurveyQuestionSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)

    url_path = 'choices'
    url_name = 'choices'
    model = QuestionChoice
    model_serializer = QuestionChoiceSerializer

    def get_queryset_with_filter(self):
        today = timezone.now()
        return self.filter_queryset(self.get_queryset()).filter(survey__end_date__gte=today).filter(
            survey__start_date__lte=today)

    @staticmethod
    def check_date(request, instance):
        today = timezone.now()
        if not instance.survey.start_date <= today <= instance.survey.end_date and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'question not available'})

    def get_instance_objects(self, pk):
        return self.model.objects.filter(question=pk)

    @action(methods=['get'], detail=True, permission_classes=[IsAdminOrReadOnly, IsAuthenticated], url_path=url_path,
            url_name=url_name)
    def action_object(self, request, pk=None):
        return super().action_object(request, pk)


class QuestionChoiceViewSet(ObjectViewSet):
    queryset = QuestionChoice.objects.order_by('id')
    serializer_class = QuestionChoiceSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated,)

    def get_queryset_with_filter(self):
        today = timezone.now()
        return self.filter_queryset(self.get_queryset()).filter(question__survey__end_date__gte=today).filter(
                question__survey__start_date__lte=today)

    @staticmethod
    def check_date(request, instance):
        today = timezone.now()
        if not instance.question.survey.start_date <= today <= instance.question.survey.end_date \
                and not request.user.is_staff:
            raise AuthenticationFailed(detail={'message': 'choices not available'})


class AnswerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        survey = serializer.validated_data['question'].survey
        user_id = self.request.user.id
        serializer.save(user_id=user_id, survey=survey)


class PassedSurveyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Survey.objects.all()
    serializer_class = PassedSurveySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            user_id = self.request.query_params.get('user_id')
            if user_id is not None:
                choices = Answer.objects.filter(user_id=user_id)
            else:
                choices = Answer.objects.all()
        else:
            choices = Answer.objects.filter(user_id=self.request.user.id)
        passed_survey = set(choices.values_list('survey_id', flat=True))
        return Survey.objects.filter(pk__in=passed_survey)


