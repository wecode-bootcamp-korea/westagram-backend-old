import json
from django.http import JsonResponse
from django.views import View
from django.core.serializers import serialize
from board.models import Board
from user.models import User


class BoardView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # login_user validation
        try:
            user_post = User.objects.get(user_name=data['user']).id
        except:
            return JsonResponse({'MESSAGE' : 'NOT_MEMBER'}, status=400)
        
        # info validation
        try:
            title = data['board_name']
            body_text = data['contents']
            image_url = data['image']
        except:
            return JsonResponse({'MESSAGE' : 'NOT_ENOUGH_INFO'}, status=400)

        # title validation
        if not Board.objects.filter(board_name=data['board_name']):
                Board.objects.create(board_name=title, user_id=user_post, image=image_url, contents=body_text)
                return JsonResponse ({'MESSAGE': 'SUCCESS'}, status=201)
        return JsonResponse({'MESSAGE' : 'TITLE_OVERLAP'}, status=400)
   
    def get(self, request):
        board_values = Board.objects.all().order_by('-id') # 최신데이터 먼저
        print(board_values)
        get_data = json.loads(serialize('json', board_values))
        return JsonResponse({'board' : get_data})
        '''
        for in_board in board_values:
            for key, value in in_board.items():
                if not key == 'id':
                    print(key, value)
            print board
            '''

# Create your views here.
