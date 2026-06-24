from django.shortcuts import render

from hotel.models import habitat


# Create your views here.
def hotel(request):
    hotel= habitat.objects.all()
    return render(request,'hotel.html', {'hotel':hotel})
