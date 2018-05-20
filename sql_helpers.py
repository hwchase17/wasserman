from contextlib import closing
import sqlalchemy
import pyodbc
import urllib

SERVER = 'TSVMLASQL01'
DATABASE = 'BasketballMaster'

CONNECTION_TEMPLATE = ('DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={server};'
                       'DATABASE={database};Trusted_Connection=yes;')

DEDUPLICATION_TEMPLATE = '''
DELETE FROM {db_name} 
WHERE CONCAT(update_time,' ',player_id,' ',year,' ', season) NOT IN
(SELECT CONCAT(MAX(update_time),' ',player_id,' ',year,' ', season)
FROM {db_name} GROUP BY player_id, year, season)
'''


def _get_connection_str(database, server_name=SERVER):
    '''Get connection string'''
    return CONNECTION_TEMPLATE.format(server=server_name, database=database)


def _get_params_from_connection_string(connection_str):
    '''Transform connection string into format to be used for params in sql connection'''
    return urllib.quote_plus(connection_str)


def _get_engine_from_connection_string(connection_str):
    '''Get sqlalchemy engine from a connection_str'''
    params = _get_params_from_connection_string(connection_str)
    return sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)


def _get_connection_to_db(connection_str):
    '''Instantiate connection to specified database'''
    return pyodbc.connect(connection_str)


def _get_basketball_connection_str():
    '''Instantiate connection to TeamWassBasketball database'''
    return _get_connection_str(DATABASE)


def _write_to_database(df, db_name, engine, if_exists='append'):
    '''Write dataframe to database'''
    with closing(engine.connect()) as con:
        df.to_sql(db_name, con, if_exists=if_exists)


def _run_query(query, engine):
    '''Execute arbitrary sql query and return results'''
    with closing(engine.connect()) as con:
        result = con.execute(query)
    return result


def update_database(db_name, df):
    '''Update database by appending new df to database and then dropping earlier values'''
    con_str = _get_basketball_connection_str()
    engine = _get_engine_from_connection_string(con_str)
    _write_to_database(df, db_name, engine)
    dedup_query = DEDUPLICATION_TEMPLATE.format(db_name=db_name)
    _run_query(dedup_query, engine)
