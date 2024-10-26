from django.urls import path
from .views import health_check, chatbot_response
urlpatterns = [
    path('health-check/', health_check),
    path('chat/', chatbot_response),
]
