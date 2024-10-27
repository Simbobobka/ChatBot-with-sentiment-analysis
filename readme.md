# ChatBot with sentimental analysis

## Overview {#intro}
Based on Django and OpenAI this simple chatbot interacts with users and performs __sentiment analysis__ on the input. The chatbot classify user messages as positive, negative, or neutral and respond accordingly. Furthermore, bot has configurable __memory__ and remembers the context of the conversation for a limited time(you could set memory duration on your own). Also chatbot asks for __feedback__ after each 3 interactions.

https://github.com/user-attachments/assets/72c98dd5-8d58-45f5-8f65-d9c99c98a54e

## Table of content
- [Overview](#intro)
- [Project installation quide](#setup-project)
    - [pipenv installation](#step2)
    - [set up project environment](#step3)
    - [setting environment variables](#step4)
    - [sentimental libraries settings](#step5)
    - [perform migrations](#step6)
    - [run server](#step7)
- [Technology Stack](#stack)
- [Additional details](#details) 

## Setup project
First of all clone this repository.

This project uses `pipenv` for managing dependencies. Follow these steps to install `pip`, `pipenv`, and set up the project. If you have ```pip``` installed go to [step 2](#step2).

### Step 1: Install `pip` (if you don't have it)

1. **Linux/macOS:** Open a terminal and run:
   ```bash
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python3 get-pip.py --user
2. **Windows:** Download the [get-pip.py](https://bootstrap.pypa.io/get-pip.py) script and run it with Python:```python get-pip.py```
Alternatively, you can use Python's package manager directly if you installed Python with the "Add Python to PATH" option.

After running these steps, check if pip was installed correctly: ```pip --version```

### Step 2: Install pipenv using pip {#step2}
Once you have pip, install pipenv by running: ```pip install pipenv```

### Step 3: Set Up the Project Environment {#step3}
Install dependencies (you should have [pipenv](https://pipenv.pypa.io/en/latest/) installed):

```pipenv install```

Activate virtual environment: 

```pipenv shell```

### Step 4: Set environment variables(required) {#step4}
This project uses environment variables for sensitive configurations like openai secret key. You should create a ```.env``` file in the __ChatAPI__ directory ``` Duanex_test_task > ChatBotSA > ChatAPI``` to store these values.

Add the following lines to your .env file, replacing the placeholders with actual values:
```
OPENAI_API_KEY=There should be your secret key
OPENAI_PROJECT_KEY=There should be your secret key for ai project
OPENAI_MODEL=gpt-4o-mini (set there any text model depend on your project opportunities)
OPENAI_MEMORY_SIZE=6 (set there memory size of model)
```

__NOTE:__
- ```OPENAI_PROJECT_KEY``` could be generated in settings in your [openai](https://platform.openai.com/) profile. It is required becouse there you should set up which ai model could be used. To add model that could be used go to __settings__ and __Limits__ tab in [openai](https://platform.openai.com/), there is __Allowed models__ article. Click edit button to add model.
- ```OPENAI_MODEL``` set model that you configure at allowed models tab.
- ```OPENAI_MEMORY_SIZE``` is a number of messages that chat remember. For instance if you set up 6, it means that history stores 3 user messanges and 3 chat`s messanges.

### Step 5: nltk settings {#step5}
The TextBlob library, which is a simple NLP (Natural Language Processing) tool that relies on certain NLTK (Natural Language Toolkit) datasets to work effectively. 

Download TextBlob Resources: In your Python shell (type ```python``` in terminal), download the required NLTK data for TextBlob: 
    
    from textblob import TextBlob
    import nltk
    nltk.download('brown')
    nltk.download('punkt') 
Write it line by line. After success downloading execute ```ctrl + z``` to exit or input ```exit()``` in terminal.

### Step 6: Perform migrations {#step6}
Execute this command from project root directory(ChatBotSA) where ```manage.py``` file is located.

Use this command to create migrations (If you recieve ```No changes detected``` it`s okey):

```python manage.py makemigrations```

Use this command to perform migrations:

```python manage.py migrate```

### Step 7: Run server {#step7}
Execute this command from project root directory(ChatBotSA) where ```manage.py``` file is located.

Use this command to start local server:

```python manage.py runserver```

Visit ```http://127.0.0.1:8000/  ``` to start chating.

## Built with {#stack}

- [Django](https://www.djangoproject.com/) - is a free and open-source, Python-based web framework that runs on a web server.
- [Openai](https://github.com/openai/openai-python) - the OpenAI Python library provides convenient access to the OpenAI REST API from any Python 3.7+ application. 
- [nltk](https://www.nltk.org/) - is a leading platform for building Python programs to work with human language data.
- [textblob](https://textblob.readthedocs.io/) - is a Python library for processing textual data.
- [django-environ](https://django-environ.readthedocs.io/) - is the Python package that allows you to use Twelve-factor methodology to configure your Django application with environment variables.

## Details {#details}

All main logic of the site is in __ChatAPI__. Visit ```views.py``` for details under the hood.
