import cgi
from datetime import datetime
import json
import pandas as pd
import requests as _requests

from constants import YEAR, SEASON_TYPES
from helpers import year_to_year_string
import nba_stats_api_constants as provider
from sql_helpers import update_database


def _get_db_name_from_measure_type(_measure_type):
    '''Consistent mapping of measure type to database name for seasons stats'''
    return 'season_{}'.format(_measure_type.lower())

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
            df.columns = map(unicode.lower, data['resultSets'][0]['headers'])
            df['year'] = year
            df['season'] = season_type
            all_df.append(df)
    all_df = pd.concat(all_df)
    all_df['update_time'] = datetime.now()
    db_name = _get_db_name_from_measure_type(measure_type)
    update_database(db_name, all_df)
