#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import os

import click

from reed import ReedClient
from util.DataProcessor import DataProcessor
from util.HTMLParser import MyHTMLParser

env_vars = os.environ.copy()


@click.group()
def cli():
    pass


@cli.command('job_search')
@click.option('--query', required=True, type=str, help='Job search query')
@click.option('--num_jobs', default=10, help='Number of jobs to show')
@click.option('--since', default=7, help='How many days back to search')
@click.option('--location', default=None, type=str,
              help='Where to perform job search')
def job_search(query, num_jobs, since, location):
    try:
        API_KEY = os.environ['API_KEY']
    except KeyError:
        print("'API_KEY' not found in environment variables.")
        return

    client = ReedClient(api_key=API_KEY)
    processor = DataProcessor()

    params = {
        'keywords': urllib.parse.quote_plus(query),
        'locationName': location
    }
    result = client.search(**params)

    all_jobs = processor.process_returned_data(result)

    relevant_jobs, date = processor.remove_irrelevant_jobs(all_jobs, since)

    if relevant_jobs.shape[0] == 0:
        print(f'Jobs posted since {date}: 0')
        return

    desired_cols = ['jobTitle',
                    'employerName',
                    'minimumSalary',
                    'locationName',
                    'jobId']

    num_rel_jobs = str(relevant_jobs.shape[0])
    print(f'Jobs posted since {date}: {num_rel_jobs}')
    print()

    for ind in relevant_jobs.index[:num_jobs]:
        job_info = relevant_jobs.iloc[ind][desired_cols]
        job_info['date'] = relevant_jobs.iloc[ind]['date'].strftime('%d %b')
        for field in job_info:
            print(field, end=' | ')
        print()
        print()


@cli.command('job_desc')
@click.option('--job_id',
              required=True,
              type=int,
              help='Reed job id')
def job_desc(job_id):
    """Simple program that displays job descriptions."""
    API_KEY = env_vars['API_KEY']
    client = ReedClient(API_KEY)
    result = client.job_details(job_id=job_id)
    job_desc_html, job_url = result['jobDescription'], result['jobUrl']
    parser = MyHTMLParser()
    print(job_url)
    parser.feed(job_desc_html)


if __name__ == '__main__':
    cli()
