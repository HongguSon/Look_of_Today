from django.shortcuts import render

# Create your views here.
def closet_main(request):
    return render(request, 'closet/closet_main.html')