import openai
from django.conf import settings

@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)

            # Configure OpenAI with your API key
            openai.api_key = settings.OPENAI_API_KEY

            # Replace "text-davinci-002" with the model you want to use
            response = openai.Completion.create(
              engine="text-davinci-002",
              prompt=f"Say hello to {name}",
              max_tokens=50
            )

            # Extract the response text
            message = response.choices[0].text.strip()

            context = {'name': name, 'message': message}
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')
