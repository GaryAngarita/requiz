from django.urls import path
from . import views

urlpatterns = [
    path('', views.cover),
    path('logreg', views.logreg),
    path('kid_register', views.kid_register),
    path('kid_login', views.kid_login),
    path('adult_login', views.adult_login),
    path('start_lite/<int:user_id>', views.start_lite),
    path('process_quiz', views.process_quiz),
    # path('quiz_heavy', views.quiz_heavy),
    path('kid_results', views.kid_results),
    path('logout', views.logout)
]
