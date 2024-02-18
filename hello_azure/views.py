from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import os
def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')

@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            openai.api_key = os.environ['OPENAI_API_KEY']#settings.OPENAI_API_KEY
            print("Request for hello page received with name=%s" % name)
            context = {'name': name }
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')
"""
import openai
from django.conf import settings


def index(request):
    print('Request for index page received')
    return render(request, 'templates/hello_azure/index.html')


def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)

            # Configure OpenAI with your API key
            #openai.api_key = process.env.OPENAI_API_KEY#settings.OPENAI_API_KEY

            # Replace "text-davinci-002" with the model you want to use
            
            response = openai.Completion.create(
              engine="gpt-3.5-turbo",
              prompt=f"Say hello to {name}",
              max_tokens=50
            )
            

            # Extract the response text
            message = "Cheese"#response.choices[0].text.strip()
            if not message:
                message = response

            context = {'name': name, 'message': message}
            return render(request, 'templates/hello_azure/hello.html', context)
    else:
        return redirect('index')
"""