DEDUPLICATION_TEMPLATE = '''
DELETE FROM {db_name} 
WHERE CONCAT(update_time,' ',player_id,' ',year,' ', season) NOT IN
(SELECT CONCAT(MAX(update_time),' ',player_id,' ',year,' ', season)
FROM {db_name} GROUP BY player_id, year, season)
'''