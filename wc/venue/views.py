from django.shortcuts import render

# Create your views here.


def venue_list(request):
    return render(request, 'venue_list.html')