from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser


from .models import Survey, SurveyQuestion, QuestionChoice
from .serializers import SurveySerializer, SurveyQuestionSerializer, QuestionChoiceSerializer
from .permissions import IsAdminOrReadOnly


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (IsAdminOrReadOnly, )


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    permission_classes = (IsAdminOrReadOnly, )


class QuestionChoiceViewSet(viewsets.ModelViewSet):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    permission_classes = (IsAdminOrReadOnly, )
