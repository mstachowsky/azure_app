from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from openai import OpenAI
import os
import traceback

def get_gpt_response(prompt):
    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI()
    print(prompt)

    # Non-streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    print(completion.choices[0].message.content)
    #print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')

def list_blobs_in_container(container_name):
    # Fetch the connection string from an environment variable
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Instantiate a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Instantiate a ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    # List all blobs in the container and return their names
    blob_names = [blob.name for blob in container_client.list_blobs()]
    return blob_names

def get_blob_content(container_name, blob_name):
    # Fetch the connection string from an environment variable
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Instantiate a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Instantiate a BlobClient
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Download the blob's contents and return as a string
    blob_content = blob_client.download_blob().readall()
    return blob_content.decode('utf-8')

@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            #openai.api_key = os.environ['OPENAI_API_KEY']
           
            prompt=f"Say hello to {name}"
            #settings.OPENAI_API_KEY
            message = 'fail'
            try:
                #response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content":prompt}],temperature=0.1)
                
                print(list_blobs_in_container("rubrics"))
                print(get_blob_content("rubrics",list_blobs_in_container("rubrics")[0]))
                message = get_gpt_response(prompt) + "".join(list_blobs_in_container("rubrics")) + "files"#response.choices[0].text.strip()

                context = {'name': name, 'message': message}
            except:
                traceback.print_exc()
            print("Request for hello page received with name=%s" % message)
            #context = {'name': name }
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