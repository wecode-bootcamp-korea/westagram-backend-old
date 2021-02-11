import json
from django.views import View
from django.http  import JsonResponse
import json
from django.utils import timezone
from .models      import Post
from user.models  import User


class postRegister(View):
  def post(self, request):
    try:
      data = json.loads(request.body)
    except :
      return JsonResponse({"message" : "JsonDecodeError"}, status = 401)

    if User.objects.get(name=data['userName']).name != data['userName'] :
      return JsonResponse({"message" : "TRUE"}, status = 401)
    
    userData = User.objects.get(name=data['userName'])
    
    postData = Post(
      userName = userData,
      content = data['content'],
      imageUrl = data['imageUrl'],
    )

    postData.save()
    # postData = Post.objects.create(userName = data['userName'], content = data['content'], imageUrl = data['imageUrl'])
    return JsonResponse({'message' : 'Connection SUCCESS'}, status = 200)
    
  
class postGet(View):
  def get(self, request):
    PostingData = Post.objects.values()
    return JsonResponse({'USERS':list(PostingData)}, status = 200)
