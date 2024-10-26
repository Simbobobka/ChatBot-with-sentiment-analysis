from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from textblob import TextBlob
from django.http import JsonResponse
from openai import OpenAI
import environ

env = environ.Env()
environ.Env.read_env()

def health_check(request):
    return HttpResponse("The project is still alive")

def welcome(request):
    return render(request, 'welcome.html')

def analyze_sentiment(user_message):
    blob = TextBlob(user_message)
    sentiment_score = blob.sentiment.polarity
    
    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"
    

def get_openai_response(user_message, sentiment, interaction_count):
    match sentiment:
        case "positive":
            prompt = f"The user is happy and said: '{user_message}'. Respond in an encouraging way. Also include apropriate happy emoji"
        case "negative":
            prompt = f"The user seems unhappy and said: '{user_message}'. Respond with an apology and offer to help. Also include apropriate unhappy emoji"
        case _:
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

    bot_response = response.choices[0].message.content
    print(interaction_count)
    if interaction_count >= 3:
        bot_response += " Could you please provide feedback about our conversation?"

    return bot_response

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        if ('interaction_count' not in request.session) or (request.session['interaction_count'] > 2):
            request.session['interaction_count'] =0
        
        sentiment = analyze_sentiment(user_message)

        request.session['interaction_count'] += 1
        interaction_count = request.session['interaction_count']

        bot_response = get_openai_response(user_message, sentiment, interaction_count)
        return JsonResponse({"response": bot_response})

    return render(request, 'main.html', {"messages": []})