import os
from functools import wraps
from flask import request
from flask import Response

class server_secret_key_required(object):
  def __init__(self, validation_funct = None):
    self.validation_funct=validation_funct
  
  def __call__(self,f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if self.validation_funct==None:
        return f(*args,**kwargs)
      auth = request.headers.get('Authorization',None)
      if self.validation_funct(auth)==False:
        resp = Response("")
        resp.status_code=401
        resp.headers['WWW-Authentication'] = 'Basic realm="Server communication"'
        return resp
      return f(*args,**kwargs)
    return decorated_function

def authorizeServerBasicEnvKey(auth):
  sec = os.environ['SERVERS_SECRET_KEY']
  if auth==None:
    return False
  if auth.startswith('Basic ')==True :
    return auth[len('Basic '):]==sec
  return False