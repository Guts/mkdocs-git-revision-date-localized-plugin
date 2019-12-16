from git import Git
from datetime import datetime
import timeago
from babel.dates import format_date

class Util:

    def __init__(self):
        self.g = Git()

    def get_revision_date_for_file(self, path: str, locale: str = 'en'):
        
        unix_timestamp =  self.g.log(path, n=1, date='short', format='%at')
        if not unix_timestamp:
            revision_date = datetime.now()
            print('WARNING -  %s has no git logs, revision date defaulting to today\'s date' % path)
        else:
            revision_date = datetime.utcfromtimestamp(int(unix_timestamp))

        # Localized versions
        revision_dates = {
            'date' : format_date(revision_date, format="long", locale=locale), 
            'datetime' : format_date(revision_date, format="long", locale=locale) + ' ' +revision_date.strftime("%H:%M:%S"),
            'iso_date' : revision_date.strftime("%Y-%m-%d"), 
            'iso_datetime' : revision_date.strftime("%Y-%m-%d %H:%M:%S"), 
            'timeago' : timeago.format(revision_date, locale = locale)
        }
    
        return revision_dates