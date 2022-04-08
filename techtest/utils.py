import json

from django.http.response import HttpResponse

from techtest.users.models import User


def json_response(data={}, status=200):
    return HttpResponse(
        content=json.dumps(data), status=status, content_type="application/json"
    )


# could only be used is some part of the views
def verify_user_token(request):
    try:
        access_token = request.headers.get('TOKEN')
        if not access_token or access_token == '':
            return False
        if User.objects.filter(token=access_token).exists():
            return True
    except Exception as a:
        print(a)
        return False
