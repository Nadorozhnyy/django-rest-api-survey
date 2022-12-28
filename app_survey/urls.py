from rest_framework import routers
from .api import SurveyViewSet, SurveyQuestionViewSet, QuestionChoiceViewSet, AnswerViewSet, PassedSurveyViewSet


app_name = 'app_survey'

router = routers.DefaultRouter()
router.register('survey', SurveyViewSet, basename='survey')
router.register('questions', SurveyQuestionViewSet)
router.register('questions_choices', QuestionChoiceViewSet)
router.register('answer', AnswerViewSet)
router.register('passed_survey', PassedSurveyViewSet, basename='passed_survey')


urlpatterns = [

]

urlpatterns += router.urls
