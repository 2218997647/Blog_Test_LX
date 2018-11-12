import functools
from flask import session,jsonify,g
from lx_blog.utils.response_code import RET
#some tool common we define

from werkzeug.routing import BaseConverter
class ReConverter(BaseConverter):
    def __init__(self,url_map,regex):
        super(ReConverter, self).__init__(url_map)
        self.regex=regex

#define a @ for validate the login state
def login_required(func):
    #func wraps will make the attribute of the inner func of wrapper as a attribute of the func decorated
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        #check the login state
        user_id=session.get("user_id")
        #if the user is login ,run the view func......
        if user_id is not None:
            #to save the user_id into g,so it can be get via g in the view func
            g.user_id=user_id
            return func(*args,**kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="please login")
    return wrapper
