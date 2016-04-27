import uuid
import urllib.parse
import psycopg2
import psycopg2.extras
from oauth2client.client import  OAuth2Credentials
from iotmirror_commons.oauth_commons import OAuthDatabase

class OAuth2StatesDatabase(OAuthDatabase):
  def __init__(self, db_url, table_name):
    super().__init__(db_url, table_name)
    
  def insertState(self, state_uuid, user_id):
    suuid = self._uuid_as_string(state_uuid)
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("INSERT INTO "+self.table_name+"(state_uuid,user_id) VALUES(%s,%s);", [suuid, user_id])
    finally:
      con.close()
  
  def getState(self, state_uuid):
    suuid = self._uuid_as_string(state_uuid)
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("SELECT state_uuid, user_id FROM "+self.table_name+" WHERE state_uuid=%s;", [suuid])
          return cur.fetchone()
    finally:
      con.close()
  
  def deleteState(self, state_uuid):
    suuid = self._uuid_as_string(state_uuid)
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE state_uuid=%s;", [suuid])
    finally:
      con.close()
  
  def deleteUserStates(self, user_id):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE user_id=%s;", [user_id])
    finally:
      con.close()
  
  @staticmethod
  def _uuid_as_string(state_uuid):
    if isinstance(state_uuid,uuid.UUID):
      return str(state_uuid)
    else:
      return state_uuid

class AccessTokensDatabase(OAuthDatabase):
  def __init__(self, db_url, table_name):
    super().__init__(db_url, table_name)
    
  def insertUserTokens(self, user_id, access_token, refresh_token = None):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("INSERT INTO "+self.table_name+"(user_id, access_token, refresh_token) VALUES(%s,%s,%s);", [user_id, access_token, refresh_token])
    finally:
      con.close()
  
  def updateUserAccessToken(self, user_id, access_token):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("UPDATE "+self.table_name+" SET access_token=%s WHERE user_id=%s;", [access_token, user_id])
    finally:
      con.close()
  
  def updateUserRefreshToken(self, user_id, refresh_token):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("UPDATE "+self.table_name+" SET refresh_token=%s WHERE user_id=%s;", [refresh_token, user_id])
    finally:
      con.close()
  
  def updateUserTokens(self, user_id, access_token, refresh_token):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("UPDATE "+self.table_name+" SET access_token=%s, refresh_token=%s WHERE user_id=%s;", [access_token, refresh_token, user_id])
    finally:
      con.close()
  
  def getUserTokens(self, user_id):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("SELECT access_token, refresh_token FROM "+self.table_name+" WHERE user_id=%s;", [user_id])
          return cur.fetchone()
    finally:
      con.close()
  
  def deleteUserTokens(self, user_id):
    try:
      with self.getConnection() as con:
        with con.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
          cur.execute("DELETE FROM "+self.table_name+" WHERE user_id=%s;", [user_id])
    finally:
      con.close()

class CredentialsProvider(object):
  def __init__(self, client_id, client_secret, token_uri, revoke_uri, token_info_uri, user_agent = None):
    self.client_id = client_id
    self.client_secret = client_secret
    self.token_uri = token_uri
    self.revoke_uri = revoke_uri
    self.token_info_uri = token_info_uri
    self.user_agent = user_agent
  
  def getCredentials(self, access_token, refresh_token, token_expiry = None, id_token = None,
                     scopes = None, token_response = None):
    return OAuth2Credentials(access_token = access_token,
                             client_id = self.client_id,
                             client_secret = self.client_secret,
                             refresh_token = refresh_token,
                             token_expiry = token_expiry,
                             token_uri = self.token_uri,
                             user_agent = self.user_agent,
                             revoke_uri = self.revoke_uri,
                             id_token = id_token,
                             token_response = token_response,
                             scopes = scopes,
                             token_info_uri = self.token_info_uri
                            )
