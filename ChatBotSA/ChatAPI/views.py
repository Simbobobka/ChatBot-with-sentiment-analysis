from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from textblob import TextBlob
from openai import OpenAI
import environ

env = environ.Env()
environ.Env.read_env()

def health_check(request):
    '''This function only used to check if app is still running.'''
    return HttpResponse("The project is still alive")

def welcome(request):
    '''This function render welcome page'''
    return render(request, 'welcome.html')

def analyze_sentiment(user_message:str) -> str:
    ''' 
    This function recieve user messange and perform sentimental analyses. 
    It asign score depending on content of the text. 
    Neutral has 0 scores,  positive > 1 and negative < 0 
    '''
    blob = TextBlob(user_message)
    sentiment_score = blob.sentiment.polarity
    
    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"
    

def get_openai_response(user_message: str, sentiment: str, interaction_count: int, history: list) -> str:
    ''' 
    This function responsible for interaction with AI. It takes 4 arguments:
    user_message      : last message that user type
    sentiment         : result of sentimental analises
    interaction_count : number that indicate interactions was made to ask for feedback (0 < interaction_count <= 3)
    history           : contain messanges history 
    '''
    
    # rules how to act depending on sentimantal results
    match sentiment:
        case "positive":
            system_message = "The user is happy. Respond in an encouraging way. Also include appropriate happy emoji."
        case "negative":
            system_message = "The user seems unhappy. Respond with an apology and offer to help. Also include appropriate unhappy emoji."
        case _:
            system_message = "The user is neutral. Ask if there’s any way to assist further. Also include appropriate emoji."
    
    messages = [{"role": "system", "content": system_message}]    
    messages.extend(history)    
    messages.append({"role": "user", "content": user_message})

    # ai set up
    client = OpenAI(
        api_key=env("OPENAI_API_KEY"),
        project=env("OPENAI_PROJECT_KEY"),
    )

    response = client.chat.completions.create(
        messages=messages,
        model=env("OPENAI_MODEL"),
        max_tokens=50,
        temperature=0.7
    )

    # feedback tracking
    bot_response = response.choices[0].message.content
    if interaction_count >= 3:
        bot_response += " Could you please provide feedback about our conversation?"

    return bot_response

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        # track interaction
        if ("interaction_count" not in request.session) or (request.session["interaction_count"] > 2): 
            request.session["interaction_count"] = 0

        # track history
        if "messages" not in request.session: 
            request.session["messages"] = []       

        # user story
        request.session['messages'].append({"role": "user", "content": user_message}) 
        
        # delete messange from story due to limit
        if len(request.session['messages']) > int(env("OPENAI_MEMORY_SIZE")): 
            request.session['messages'].pop(0)  

        # add interacton score
        request.session["interaction_count"] += 1

        # all paremeters that would be passed to bot
        sentiment = analyze_sentiment(user_message)
        interaction_count = request.session["interaction_count"]
        history = [{"role": msg["role"], "content": msg["content"]} for msg in request.session['messages']]
        
        # send prompt to bot
        bot_response = get_openai_response(user_message, sentiment, interaction_count, history)

        # bot history
        request.session['messages'].append({"role": "assistant", "content": bot_response}) 
        if len(request.session['messages']) > int(env("OPENAI_MEMORY_SIZE")):
            request.session['messages'].pop(0)

        return JsonResponse({"response": bot_response})
    return render(request, "main.html", {"messages": request.session.get("messages", [])})