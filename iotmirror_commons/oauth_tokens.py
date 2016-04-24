import urllib.parse
import psycopg2
import psycopg2.extras

class TokensDatabase:
  def __init__(self, db_url, table_name=""):
    self.url = urllib.parse.urlparse(db_url)
    self.table_name=table_name
    
  def getConnection(self):
    return psycopg2.connect(database=self.url.path[1:], user=self.url.username,
                            password=self.url.password,host=self.url.hostname,
                            port=self.url.port
                           )

class AccessTokensDatabase(TokensDatabase):
  def __init__(self, db_url, table_name=""):
    super().__init__(db_url,table_name)
  
  def insertUserAccessTokens(self,userID,access_token, access_token_secret):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("INSERT INTO "+self.table_name+"(user_id, access_token, access_token_secret) VALUES(%s,%s,%s);",[userID, access_token, access_token_secret])
    finally:
      con.close()
      
  def updateUserAccessTokens(self,userID,access_token, access_token_secret):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("UPDATE "+self.table_name+" SET access_token=%s, access_token_secret=%s WHERE user_id=%s;",[access_token, access_token_secret,userID])
    finally:
      con.close()
  
  def getUserAccessTokens(self, userID):
    try:
      row = None
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("SELECT access_token, access_token_secret FROM "+self.table_name+" WHERE user_id=%s;",[userID])
          row = cur.fetchone()
      return row
    finally:
      con.close()
  
  def deleteUserAccessTokens(self, userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE user_id=%s;",[userID])
    finally:
      con.close()

class RequestTokensDatabase(TokensDatabase):
  def __init__(self, db_url, table_name=""):
    super().__init__(db_url,table_name)
  
  def insertRequestToken(self, request_token,request_token_secret,userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("INSERT INTO "+self.table_name+"(request_token, request_token_secret, user_id) VALUES(%s,%s,%s);",[request_token, request_token_secret, userID])
    finally:
      con.close()
      
  def getRequestToken(self, request_token):
    try:
      row = None
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("SELECT request_token, request_token_secret, user_id FROM "+self.table_name+" WHERE request_token=%s;",[request_token])
          row = cur.fetchone()
      return row
    finally:
      con.close()
      
  def deleteRequestToken(self, request_token):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE request_token=%s;",[request_token])
    finally:
      con.close()
      
  def deleteUserRequestTokens(self, userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE user_id=%s;",[userID])
    finally:
      con.close()