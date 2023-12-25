from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # index urls
    path('', index_view, name='index_url'),
    path('site/', home_view),
    path('services/', service_view),
    path('calorie/', calorie_view),
    path('food/', food_view),
    path('disease/', disease_view),

    #cabinet
    path('sign-up/', sign_up),
    path('post-daily-plan/', daily_plan),
    path('get-plan/', getuserpost),
    path('edit-plan/<int:pk>/', edit_plan),
    path('delete-plan/<int:pk>/', delete_plan),
    path('post-question/', post_question),
    path('questions/', get_question),
    path('my-questions/', get_my_questions),
    path('edit-question/<int:pk>/', edit_question),
    path('delete-question/<int:pk>/', delete_question),
    path('post-diet/', post_diet),
    path('my-diet/', get_my_diet),
    path('edit-diet/<int:pk>/', edit_diet),
    path('delete-diet/<int:pk>/', delete_diet),
    path('notification/', notification_alert),


    # token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #cabinet
    path('register/', register_view, name='register_url')
]
