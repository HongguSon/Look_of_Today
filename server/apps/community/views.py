# from django.http import JsonResponse
# from django.shortcuts import render
# from server.apps.main.models import Comment
# import json

# # Create your views here.
# def community_main(request):
#     return render(request, 'community/community.html')

# def post_create(request):
#     return render(request, 'community/post_create.html')

# def post_detail(request):
#     return render(request, 'community/post_detail.html')

# # @csrf_exempt
# def comment(request):
#     jsonobject = json.loads(request.body)

#     comment = Comment.objects.create(
#         title=jsonobject.get('boardId'),
#         author=jsonobject.get('memberId'),
#         content=jsonobject.get('content'))
#     comment.save()

#     context = {
#         'author' : comment.author,
#         'content' : comment.content,
#         'create_Date' : comment.create_date,
#         'update_Date' : comment.update_date,
#     }
    
#     return JsonResponse(context);
