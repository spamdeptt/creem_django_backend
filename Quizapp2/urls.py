from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('creamcards', views.CreamCardsViewSet)
router.register('questions', views.QuizQuestionsViewSet)
router.register('q_collection', views.QuizQuestionsCollectionViewSet)
router.register('ccfresh', views.FreshCreamCardsViewSet)
router.register('correct', views.QuizQuestionCorrectViewSet)
router.register('incorrect', views.QuizQuestionIncorrectViewSet)

urlpatterns = router.urls

