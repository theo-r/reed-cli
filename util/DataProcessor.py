import pandas as pd
from datetime import datetime, timedelta


class DataProcessor():

    def __init__(self):
        pass

    @staticmethod
    def fix_day_month(x):
        if x > datetime.now():
            return datetime(x.year, x.day, x.month)
        else:
            return x

    def process_returned_data(self, job_data):
        all_jobs = pd.DataFrame(job_data)
        all_jobs['date'] = pd.to_datetime(all_jobs['date'])
        all_jobs['date'] = [self.fix_day_month(x) for x in all_jobs['date']]
        return all_jobs

    def remove_irrelevant_jobs(self, df, since):
        date = str(datetime.now().date() + timedelta(days=-since))

        # terms_to_avoid = 'Senior|Lead|Principal|Apprentice' \
        #     '|Director|Manager|Head'

        terms_to_avoid = 'Director'

        relevant_jobs = (df[~df.jobTitle.str.contains(terms_to_avoid)]
                         .query('date > @date')
                         .sort_values('date', ascending=False)
                         .reset_index()
                         .drop(columns='index'))
        return relevant_jobs, date
