from django.shortcuts import render

# Create your views here.


def index(request, id):
    return render(request, 'overview/index.html', {
        'id': id
    })
