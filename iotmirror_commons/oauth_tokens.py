import urllib.parse
import psycopg2
import psycopg2.extras
from iotmirror_commons.oauth_commons import OAuthDatabase

class AccessTokensDatabase(OAuthDatabase):
  def __init__(self, db_url, table_name):
    super().__init__(db_url, table_name)
  
  def insertUserToken(self, userID, access_token, access_token_secret):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("INSERT INTO "+self.table_name+"(user_id, access_token, access_token_secret) VALUES(%s,%s,%s);", [userID, access_token, access_token_secret])
    finally:
      con.close()
      
  def updateUserToken(self, userID, access_token, access_token_secret):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("UPDATE "+self.table_name+" SET access_token=%s, access_token_secret=%s WHERE user_id=%s;", [access_token, access_token_secret, userID])
    finally:
      con.close()
  
  def getUserToken(self, userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("SELECT access_token, access_token_secret FROM "+self.table_name+" WHERE user_id=%s;", [userID])
          return cur.fetchone()
    finally:
      con.close()
  
  def deleteUserTokens(self, userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE user_id=%s;", [userID])
    finally:
      con.close()

class RequestTokensDatabase(OAuthDatabase):
  def __init__(self, db_url, table_name):
    super().__init__(db_url, table_name)
  
  def insertToken(self, request_token,request_token_secret,userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("INSERT INTO "+self.table_name+"(request_token, request_token_secret, user_id) VALUES(%s,%s,%s);",[request_token, request_token_secret, userID])
    finally:
      con.close()
      
  def getToken(self, request_token):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("SELECT request_token, request_token_secret, user_id FROM "+self.table_name+" WHERE request_token=%s;",[request_token])
          return cur.fetchone()
    finally:
      con.close()
      
  def deleteToken(self, request_token):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE request_token=%s;",[request_token])
    finally:
      con.close()
      
  def deleteUserTokens(self, userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE user_id=%s;", [userID])
    finally:
      con.close()
