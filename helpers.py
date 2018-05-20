def year_to_year_string(year):
    '''Transform a year (YYYY) to a year string (YYYY-YY)'''
    last_two_digits = str(year % 100 + 1).zfill(2)
    return '{}-{}'.format(year, last_two_digits)
