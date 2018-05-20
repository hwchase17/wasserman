import cgi
from datetime import datetime
import json
import pandas as pd
import requests as _requests

from constants import YEAR, SEASON_TYPES
from helpers import year_to_year_string
import nba_stats_api_constants as provider


for measure_type in provider.SUMMARY_STATS_TYPES:
    all_df = []
    for year in range(YEAR, YEAR + 1):
        for season_type in SEASON_TYPES:
            year_id = year_to_year_string(year)
            api_params = provider.get_season_stats_api_params(measure_type, year_id, season_type)
            pull_url = cgi.urlparse.urljoin(provider.BASE_URL, provider.SEASON_SUMMARY_STATS_URL)
            response = _requests.get(pull_url, params=api_params, headers=provider.HEADER_DATA)
            data = json.loads(response.content)
            df = pd.DataFrame(data['resultSets'][0]['rowSet'])
            df.columns = data['resultSets'][0]['headers']
            df['Year'] = year
            df['season'] = season_type
            all_df.append(df)
    all_df = pd.concat(all_df)
    all_df['AGE'] = all_df['AGE'].astype(int)
    all_df = all_df.replace({',': ''}, regex=True)
    all_df = all_df.fillna(0)
    all_df['season'] = all_df['season'].str.replace('Regular Season', 'reg')

    all_df['dbTime'] = datetime.now()
    del all_df['NBA_FANTASY_PTS']
    del all_df['NBA_FANTASY_PTS1']
    columns = [col for col in all_df.columns if 'RANK' not in col]
    all_df.to_csv('C:\\Users\\hchase\\Documents\\SQLReportCode\\CSV\\season' + type + '.csv',
                  index=False)
    import pyodbc

    server = 'TSVMLASQL01'
    database = 'TeamWassBasketball'

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    query = '''
	BULK INSERT season{} FROM 'C:\\Users\\hchase\\Documents\\SQLReportCode\\CSV\\season{}.csv'
                    WITH
                    (
                    FIRSTROW = 2,
                    FIELDTERMINATOR = ',',  --CSV field delimiter
                    ROWTERMINATOR = '\n',   --Use to shift the control to next row
                    TABLOCK
                    )
	'''.format(type, type)
    cursor.execute(query)
    query = '''
	DELETE 
  	FROM season{} WHERE CONCAT(dbdate,' ',playerId,' ',season,' ', seasonType) NOT IN
                      (
                      SELECT CONCAT(MAX(dbdate),' ',playerId,' ',season,' ', seasonType)
                      FROM season{} GROUP BY playerId, season, seasonType)
	'''.format(type, type)
    cursor.execute(query)
