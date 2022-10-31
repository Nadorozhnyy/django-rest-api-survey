from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


from .models import Survey, SurveyQuestion, QuestionChoice
from .serializers import SurveySerializer, SurveyQuestionSerializer, QuestionChoiceSerializer
from .permissions import IsAdminOrReadOnly


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (IsAdminOrReadOnly, )

    @action(methods=['get'], detail=True, permission_classes=[IsAdminOrReadOnly], url_path='questions',
            url_name='questions')
    def questions(self, request, pk=None):
        questions = SurveyQuestion.objects.filter(survey=pk)
        serializer = SurveyQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @staticmethod
    def timezone_validation(self, request):
        if request.user.is_staff:
            survey = Survey.objects.all()
        else:
            today = timezone.now()
            survey = Survey.objects.filter(end_date__gte=today).filter(start_date__lte=today)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            survey = Survey.objects.all()
        else:
            today = timezone.now()
            survey = Survey.objects.filter(end_date__gte=today).filter(start_date__lte=today)
        serializer = SurveySerializer(survey, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class SurveyQuestionViewSet(viewsets.ModelViewSet):

    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    permission_classes = (IsAdminOrReadOnly, )

    @action(methods=['get'], detail=True, permission_classes=[IsAdminOrReadOnly], url_path='choices',
            url_name='choices')
    def choices(self, request, pk=None):
        choices = QuestionChoice.objects.filter(question=pk)
        serializer = QuestionChoiceSerializer(choices, many=True)
        return Response(serializer.data)


class QuestionChoiceViewSet(viewsets.ModelViewSet):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    permission_classes = (IsAdminOrReadOnly, )
