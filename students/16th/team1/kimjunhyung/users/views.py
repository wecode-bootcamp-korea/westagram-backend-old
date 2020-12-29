import json

from django.views   import View
from django.http    import JsonResponse

from .models            import User
from decorators.utils   import check_blank

class UserSignupView(View):
    @check_blank
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]

        user = User.objects.filter(email = email)
        if user.exists():
            return JsonResponse({"message":"USER_ALREADY_EXIST"}, status = 400)
        if len(password) < 8:
            return JsonResponse({"message":"PASSWORD_IS_AT_LEAST_8"}, status = 400)
        User.objects.create(email = email, password = password)         
        return JsonResponse({"message":"SUCCESS"}, status = 200)


            