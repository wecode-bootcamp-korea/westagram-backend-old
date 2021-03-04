from json

from django.views import View

from .models import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        