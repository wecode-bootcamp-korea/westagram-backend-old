import json
from django.http import JsonResponse
from django.views import View
from django.core.serializers import serialize
from board.models import Board, Comment
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
        # empty_board validation
        try:
            board_values = Board.objects.all().order_by('-id') # 최신데이터 먼저
            get_data = json.loads(serialize('json', board_values))
            return JsonResponse({'board' : get_data})
        except:
            return JsonResponse({'MESSAGE' : 'EMPTY_BOARD'}, status=400)
        '''
        for in_board in board_values:
            for key, value in in_board.items():
                if not key == 'id':
                    print(key, value)
            print board
            '''

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        #login_user validation
        try:
            user_comment = User.objects.get(user_name=data['user']).id
        except:
            return JsonResponse({'MESSAGE' : 'NOT_MEMBER'}, status=400)

        # board validation
        try:
            board_comment = Board.objects.get(board_name=data['board_title']).id
        except:
            return JsonResponse({'MESSAGE' : 'THERE ARE NO BOARD'}, status=400)

        #comment validation
        try:
            body_comment = data['comment_body']
            Comment.objects.create(board_title_id=board_comment, comment_user_id=user_comment, comment_body=body_comment)
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except:
            return JsonResponse({'MESSAGE' : 'NOT_COMMNET'}, status=400)

    def get(self, request):
        '''
        all of comments
        try:
            comment_values = Comment.objects.all()
            get_comment_data = json.loads(serialize('json', comment_values))
            return JsonResponse({'comment' : get_comment_data})
        except:
            return JsonResponse({'MESSAGE' : 'NO_COMMENT'}, status=400)
        '''

        # first_board_comments
        try:
            first_board = Board.objects.first()
            comment_values_first = Comment.objects.filter(board_title_id=first_board)
            get_comment_first_data = json.loads(serialize('json', comment_values_first))
            return JsonResponse({'COMMENT' : get_comment_first_data })
        except:
            return JsonResponse({'MESSAGE' : 'EMPTY_DATA'}, status=400)
# Create your views here.
