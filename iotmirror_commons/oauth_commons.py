import urllib.parse
import psycopg2

class OAuthDatabase(object):
  def __init__(self, db_url, table_name):
    self.url = urllib.parse.urlparse(db_url)
    self.table_name = table_name
    
  def getConnection(self):
    return psycopg2.connect(database = self.url.path[1:], user = self.url.username,
                            password = self.url.password,host = self.url.hostname,
                            port = self.url.port
                           )
