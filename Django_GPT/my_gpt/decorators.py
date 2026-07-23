from functools import wraps
from urllib.parse import urlencode
from django.shortcuts import redirect

def model_login_required(view_func):
    """
    로그인 안 된 사용자가 접근하면
    /accounts/login/?next=<원래경로>&required=1 로 보낸다.
    login.html에서 required=1을 보고 alert를 띄운다.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            query = urlencode(
                {
                    "next": request.path,
                    "required": "1",
                }
            )
            return redirect(f"/accounts/login/?{query}")

        return view_func(request, *args, **kwargs)

    return wrapper
