from django.urls import path

from .moderator import *
from .user import *
from .news import *
from .food import *
from .quiz import *
from .sprint import *
from .admin_ops import super_ops, logout
from middleware import wrap_path_middleware
from ..middleware import admin_is_authenticated

app_name = 'admin'


base_patterns = [
    path("super", super_ops, name="super"),
    path("logout", logout, name="logout"),
    
    path("user/<str:uuid>", user, name="user"),
    path("users", users, name="users"),
    
    path("moderators", moderator_view, name="moderators"),
    path("moderator/<str:uuid>", moderator, name="moderator"),
    
    path("news/<str:uuid>", news, name="news"),
    path("news", news_view, name="news_view"),
    
    path("food/category/<str:uuid>", food_category, name="food_category"),
    path("food/category", food_categories, name="food_categories"),
    path("food/of/<str:uuid>", foods_of_category, name="foods_of_category"),
    path("food/<str:uuid>", food, name="food"),
    
    path("quizzes", quizzes, name="quizzes"),
    path("quiz/<str:uuid>", quiz, name="quiz"),
    path("quiz/<str:uuid>/questions", quiz_questions, name="quiz_questions"),
    path("quiz/question/<str:uuid>", quiz_question, name="quiz_question"),
    
    path("sprints/quizzes", quizzes_sprints, name="quizzes_sprints"),
    path("sprints/quiz/<str:uuid>/users", quiz_users_sprints, name="quiz_users_sprints"),
    path("sprints/quiz/<str:quiz>/<str:user>", quiz_user_sprints, name="quiz_user_sprints"),
    path("sprint/<str:uuid>/answers", quiz_sprint_answers, name="quiz_sprint_answers"),
    
    path("sprint/answer/<str:uuid>/verify", sprint_answer_verify, name="sprint_answer_verify"),
]

# urlpatterns = base_patterns
urlpatterns = wrap_path_middleware(admin_is_authenticated(), base_patterns)
