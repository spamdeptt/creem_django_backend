from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('students', views.StudentViewSet)
router.register('creamcards', views.CreamCardsViewSet, basename='creamcards')
router.register('blogcardbutton', views.BlogCardButtonViewSet, basename='blogcardbutton')
router.register(r'published-creamcards-ids', views.PublishedCreamCardsIDViewSet, basename='published-creamcards-ids')
# router.register('questions', views.QuizQuestionsViewSet) //removed because not needed
router.register('q_collection', views.QuizQuestionsCollectionViewSet)
#there is no point in exposing the questions list -- only detail view is to be used
# so create a custom viewset like done in 4.4
router.register('correct', views.QuizQuestionCorrectViewSet)
router.register('incorrect', views.QuizQuestionIncorrectViewSet)
router.register('trending', views.TrendingTopicsViewSet)
router.register('trendingarchive', views.TrendingArchiveViewSet)
router.register('fltcollections', views.FLTCollectionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

