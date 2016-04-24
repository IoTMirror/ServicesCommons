import urllib.parse
import psycopg2
import psycopg2.extras

class OAuthTokensDatabase:
  def __init__(self, db_url, table_prefix=""):
    self.url = urllib.parse.urlparse(db_url)
    self.table_prefix=table_prefix
  
  def insertUserAccessTokens(self,userID,access_token, access_token_secret):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("INSERT INTO "+self.table_prefix+"access_tokens(user_id, access_token, access_token_secret) VALUES(%s,%s,%s);",[userID, access_token, access_token_secret])
    finally:
      con.close()
      
  def updateUserAccessTokens(self,userID,access_token, access_token_secret):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("UPDATE "+self.table_prefix+"access_tokens SET access_token=%s, access_token_secret=%s WHERE user_id=%s;",[access_token, access_token_secret,userID])
    finally:
      con.close()
  
  def getUserAccessTokens(self, userID):
    try:
      row = None
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("SELECT access_token, access_token_secret FROM "+self.table_prefix+"access_tokens WHERE user_id=%s;",[userID])
          row = cur.fetchone()
      return row
    finally:
      con.close()
  
  def deleteUserAccessTokens(self, userID):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_prefix+"access_tokens WHERE user_id=%s;",[userID])
    finally:
      con.close()
    
  def getConnection(self):
    return psycopg2.connect(database=self.url.path[1:], user=self.url.username,
                            password=self.url.password,host=self.url.hostname,
                            port=self.url.port
                           )