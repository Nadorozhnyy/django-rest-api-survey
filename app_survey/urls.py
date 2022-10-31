from rest_framework import routers
from django.urls import path, include
from .api import SurveyViewSet, SurveyQuestionViewSet, QuestionChoiceViewSet


app_name = 'app_survey'

router = routers.DefaultRouter()
router.register('survey', SurveyViewSet)
router.register('questions', SurveyQuestionViewSet)
router.register('questions_choices', QuestionChoiceViewSet)

urlpatterns = [

]

urlpatterns += router.urls
