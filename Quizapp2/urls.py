from django.urls import path
from . import views

urlpatterns = [
    path("creamcards/", views.CreamCardsList.as_view()),
    path("creamcards/fresh_2", views.FreshCreamCards_delta2.as_view()),
    path("creamcards/<int:pk>", views.CreamCardDetail.as_view()),

    path('questions/', views.QuizQuestionsList.as_view()),
    path('questions/<int:pk>', views.QuizQuestionDetail.as_view()),

    path('questions/collection/', views.QuizQuestionCollectionList.as_view()),
    path('questions/collection/<int:pk>', views.QuizQuestionCollectionDetail.as_view()),
    
    path('questions/correct/<int:pk>', views.QuizQuestionsCorrect.as_view()),
    path('questions/incorrect/<int:pk>', views.QuizQuestionsIncorrect.as_view()),
    
]

