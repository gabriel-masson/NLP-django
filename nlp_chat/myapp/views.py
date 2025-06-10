from django.shortcuts import render, HttpResponse


def home(request):
    """
    Render the home page.
    """
    return render(request, 'home.html')
    # return HttpResponse("Welcome to the NLP Chat Application!")
