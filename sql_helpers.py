from datetime import datetime
import pyodbc

SERVER = 'TSVMLASQL01'
DATABASE = 'TeamWassBasketball'

CONNECTION_TEMPLATE = ('DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={server};'
                       'DATABASE={database};Trusted_Connection=yes;')

DEDUPLICATION_TEMPLATE = query = '''
DELETE FROM {db_name} 
WHERE CONCAT(dbdate,' ',playerId,' ',season,' ', seasonType) NOT IN
(SELECT CONCAT(MAX(dbdate),' ',playerId,' ',season,' ', seasonType)
FROM {db_name} GROUP BY playerId, season, seasonType)
'''


def _get_connection_to_db(database, server_name=SERVER):
    '''Instantiate connection to specified database'''
    return pyodbc.connect(CONNECTION_TEMPLATE.format(server=server_name, database=database))


def _get_basketball_connection():
    '''Instantiate connection to TeamWassBasketball database'''
    return _get_connection_to_db(DATABASE)


def update_database(db_name, df):
    '''Update database by appending new df to database and then dropping earlier values'''
    df['dbTime'] = datetime.now()
    con = _get_basketball_connection()
    df.to_sql(db_name, con, if_exists='append')
    dedup_query = DEDUPLICATION_TEMPLATE.format(db_name=db_name)
    con.cursor().execute(dedup_query)
