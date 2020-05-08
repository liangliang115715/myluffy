

class CommonException(Exception):

    def __init__(self,code,msg):
        self.code = code
        self.msg = msg

class LoginException(Exception):

    def __init__(self,msg):
        self.msg = msg
