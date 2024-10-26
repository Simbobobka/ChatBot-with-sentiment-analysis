from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from textblob import TextBlob
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI
import environ

env = environ.Env()
environ.Env.read_env()

def health_check(request):
    return HttpResponse("The project is still alive")

def analyze_sentiment(user_message):
    blob = TextBlob(user_message)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"
    

def get_openai_response(user_message, sentiment):
    if sentiment == "positive":
        prompt = f"The user is happy and said: '{user_message}'. Respond in an encouraging way. Also include apropriate emoji"
    elif sentiment == "negative":
        prompt = f"The user seems unhappy and said: '{user_message}'. Respond with an apology and offer to help. Also include apropriate emoji"
    else:
        prompt = f"The user is neutral and said: '{user_message}'. Ask if there’s any way to assist further. Also include apropriate emoji"    

    client = OpenAI(
        api_key=env("OPENAI_API_KEY"),
        project=env("OPENAI_PROJECT_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            
        model=env("OPENAI_MODEL"),
        max_tokens=50,
        temperature=0.7
    )
    return response.choices[0].message.content

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        sentiment = analyze_sentiment(user_message)
        bot_response = get_openai_response(user_message, sentiment)
        return JsonResponse({"response": bot_response})
    return JsonResponse({"error": "Invalid request"}, status=400)