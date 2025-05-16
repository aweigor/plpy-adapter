import psycopg2, os, sys
import pathlib
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Config(object):
  PG_HOST = os.getenv('PG_HOST', 'localhost')
  PG_PORT = os.getenv('PG_PORT', '5432')
  PG_USER = os.getenv('PG_USER', 'postgres')
  PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
  PG_DATABASE = os.getenv('PG_DATABASE', 'mydb')

def _connect(auth):
  host = auth['host'] if 'host' in auth else 'localhost'
  port = auth['port'] if 'port' in auth else '5432'
  user = auth['user'] if 'user' in auth else 'postgres'
  password = auth['password'] if 'password' in auth else 'postgres'
  database = auth['database'] if 'database' in auth else 'mydb'
  conn = None
  try:
    conn = psycopg2.connect(host=host,
                            port=port,
                            user=user,
                            password=password,
                            database=database)
    cur = conn.cursor()
    return conn, cur
  except (Exception, psycopg2.DatabaseError) as error:
    raise error

class PgQuery(object):

  @staticmethod
  def execute(auth={}, query=''):
    conn, cursor = _connect(auth)
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()
    return True


if __name__ == "__main__":
  args = sys.argv[1:]

  if len(args) == 0:
    sys.exit("Syntax: run.py <file_path_to_execute>")

  cwd = pathlib.Path().resolve()
  plscript = pathlib.Path("{cwd}/plscripts/{script}.py".format(cwd = cwd, script = args[0]))

  if not plscript.is_file():
    sys.exit("No such script: {script}".format(script = plscript.name))

  auth = {
    'host': Config.PG_HOST,
    'user': Config.PG_USER,
    'port': Config.PG_PORT,
    'password': Config.PG_PASSWORD,
    'database': Config.PG_DATABASE,
  }

  query = '''
  DO $$
      import importlib.util
      spec = importlib.util.spec_from_file_location("executable", "{path}")
      executable = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(executable)
      executable.main(plpy)
  $$ LANGUAGE plpython3u;
  '''.format(path = plscript)

  PgQuery.execute(auth=auth, query=query)
