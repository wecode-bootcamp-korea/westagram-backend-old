import json

from django.http      import JsonResponse
from django.views     import View

from user.models  import User, Follow
from user.utils   import login_required


class FollowView(View):
    # 1. 인증
    @login_required
    def post(self, request):
        print("================= 팔로우 절차 기동 =================")

        # 2. 필수값 검사
        try:
            to_user_id = json.loads(request.body)['to_user_id']
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 3. 사용자가 자기 자신을 follow 하는지 확인
        from_user_id = request.user_id
        if str(from_user_id) == to_user_id:
            return JsonResponse({'MESSAGE': 'SELF_FOLLOW_NOT_ALLOWED'}, status=401)

        # 4. 사용자가 현재 to_user_id 에 이미 follow 상태인지 확인
        to_user = User.objects.get(id=to_user_id)
        if Follow.objects.filter(to_user=to_user, from_user=from_user_id).exists():
            return JsonResponse({'MESSAGE': 'FOLLOW_DUPLICATION'}, status=401)

        # 5. DB에 데이터 작성
        try:
            Follow.objects.create(from_user_id=from_user_id, to_user_id=to_user_id)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({"MESSAGE": "INVALID_PAYLOAD"}, status=400)

        # 6. 모든 과정 통과 -> 201 리턴
        print("================= 팔로우 정상 종료 =================")
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


class UnFollowView(View):
    # 1. 인증
    @login_required
    def post(self, request):
        print("================= 언팔로우 절차 기동 =================")

        # 2. 필수값 검사
        try:
            to_user_id = json.loads(request.body)['to_user_id']
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 3. 사용자가 현재 to_user_id 에 follow 상태에 있는지 확인
        from_user_id = request.user_id
        follow_relationship = Follow.objects.filter(to_user_id=to_user_id, from_user_id=from_user_id)
        if not follow_relationship.exists():
            return JsonResponse({'MESSAGE': 'NOT_IN_FOLLOW_RELATIONSHIP'}, status=401)

        # 4. DB 에서 팔로우 데이터 삭제
        try:
            follow_relationship.delete()
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "INVALID_PAYLOAD"}, status=400)

        # 5. 모든 과정 통과 -> 201 리턴
        print("================= 언팔로우 정상 종료 =================")
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
