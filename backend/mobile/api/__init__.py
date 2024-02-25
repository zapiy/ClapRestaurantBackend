from django.urls import path

from .user_ops import *
from .views import *

from mobile.middleware import mobile_is_authenticated
from middleware import wrap_path_middleware


app_name = 'mobile'

urlpatterns = [    
    path('auth', view=auth),
    *wrap_path_middleware(
        middleware=mobile_is_authenticated(),
        pathes=[
            path('logout', view=logout),
            path('user/data', view=user_data),
            
            path('news', view=news_view),
            
            path('food/categories', view=food_categories),
            path('food/<str:uuid>', view=foods_of_category),
            
            path('quizzes', view=quizzes),
            path('quiz/reset/<str:uuid>', view=reset_quiz_progress),
            path('quiz/solve/<str:uuid>', view=solve_quiz),
            path('quiz/next/<str:uuid>', view=get_next_quiz),
        ]
    ),
]
