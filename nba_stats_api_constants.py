HEADER_DATA = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '
                  'Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
              ',image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'
}

BASE_URL = 'http://stats.nba.com/stats/'
SEASON_SUMMARY_STATS_URL = 'leaguedashplayerstats'
SUMMARY_STATS_TYPES = ('Base', 'Advanced', 'Misc', 'Scoring', 'Usage', 'Defense')


def get_season_stats_api_params(measure_type, year_id, season_type):
    return {
        'College': '',
        'Conference': '',
        'Country': '',
        'DateFrom': '',
        'DateTo': '',
        'Division': '',
        'DraftPick': '',
        'DraftYear': '',
        'GameScope': '',
        'GameSegment': '',
        'Height': '',
        'LastNGames': 0,
        'LeagueID': '00',
        'Location': '',
        'MeasureType': measure_type,
        'Month': 0,
        'OpponentTeamID': 0,
        'Outcome': '',
        'PORound': '',
        'PaceAdjust': 'N',
        'PerMode': 'Totals',
        'Period': 0,
        'PlayerExperience': '',
        'PlayerPosition': '',
        'PlusMinus': 'N',
        'Rank': 'Y',
        'Season': year_id,
        'SeasonSegment': '',
        'SeasonType': season_type,
        'ShotClockRange': '',
        'StarterBench': '',
        'TeamID': '',
        'VsConference': '',
        'VsDivision': '',
        'Weight': ''
    }
