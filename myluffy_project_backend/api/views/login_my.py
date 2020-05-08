from rest_framework.views import APIView
from api.models import UserInfo,Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from api.utils.captcha_verify import verify
from api.utils.exceptions import LoginException
from api.utils.response import BaseResponse
import uuid,datetime

class LoginView(APIView):
    def post(self,request):
        res = {'user':None,'msg':None,'data':None}
        try:
            if not verify(request.data):
                raise LoginException('验证码错误')
            user = request.data.get('username')
            pwd = request.data.get('password')
            user_obj =authenticate(username =user,password=pwd)
            print(user_obj)
            if not user_obj:
                raise LoginException('用户名或密码错误')
            random_str =str(uuid.uuid4())
            Token.objects.update_or_create(user=user_obj,defaults={'key':random_str,'created':datetime.datetime.now()})
            # res['user'] = user_obj.username
            # res['token'] = random_str
            res['data']['user'] =user_obj.username
            res['data']['token'] =user_obj.random_str
        except LoginException as e:
            res['msg'] = e.msg
        except Exception:
            pass
        print(res)
        return Response(res)
