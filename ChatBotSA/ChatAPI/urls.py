from django.urls import path
from .views import health_check, chatbot_response, welcome
urlpatterns = [
    path('health-check/', health_check),
    path('', welcome),
    path('chat/', chatbot_response, name='chat'),
]
