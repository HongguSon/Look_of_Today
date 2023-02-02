from django.shortcuts import render

# Create your views here.
def community_main(request):
    return render(request, 'community\community.html')

def post_create(request):
    return render(request, 'community\post_create.html')