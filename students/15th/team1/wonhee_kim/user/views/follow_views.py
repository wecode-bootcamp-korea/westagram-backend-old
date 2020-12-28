import json

from django.http      import JsonResponse
from django.views     import View

from user.models  import User, Follow
from user.utils   import login_required


class FollowView(View):
    @login_required
    def post(self, request):

        to_user_id = json.loads(request.body).get('to_user_id')
        if to_user_id is None:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # follow 할 사용자가 존재하는지 확인
        to_user = User.objects.filter(id=to_user_id)
        if not to_user.exists():
            return JsonResponse({"MESSAGE": "FOLLOWED_USER_NOT_EXIST"}, status=400)

        # 사용자가 자기 자신을 follow 시도 하는지 확인
        from_user_id = request.user.id
        if str(from_user_id) == to_user_id:
            return JsonResponse({'MESSAGE': 'SELF_FOLLOW_NOT_ALLOWED'}, status=401)

        # 사용자가 현재 to_user_id 에 이미 follow 상태인지 확인
        to_user = User.objects.get(id=to_user_id)
        if Follow.objects.filter(to_user=to_user, from_user=from_user_id).exists():
            return JsonResponse({'MESSAGE': 'FOLLOW_DUPLICATION'}, status=401)

        # DB에 데이터 작성
        Follow.objects.create(from_user_id=from_user_id, to_user_id=to_user_id)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


    @login_required
    def delete(self, request):

        to_user_id = json.loads(request.body).get('to_user_id')
        if to_user_id is None:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 사용자가 현재 to_user_id 에 follow 상태에 있는지 확인
        from_user_id = request.user.id
        follow_relationship = Follow.objects.filter(to_user_id=to_user_id, from_user_id=from_user_id)
        if not follow_relationship.exists():
            return JsonResponse({'MESSAGE': 'NOT_IN_FOLLOW_RELATIONSHIP'}, status=400)

        # DB 에서 팔로우 데이터 삭제
        follow_relationship.delete()

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
