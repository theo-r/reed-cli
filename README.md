# reed-cli

Search for jobs from the command line with the Reed API and python.

This is a [click](https://click.palletsprojects.com/en/7.x/) project which
makes use of the python package [reed](https://pypi.org/project/reed/). 
To get started you will need to install the reed package on your machine using
[pip](https://pip.pypa.io/en/latest/). 

    $ pip install indeed

## API Credentials

To use the CLI you will need an key for the Reed API.
You can sign up for an API key [here](https://www.reed.co.uk/developers/jobseeker).

Once you have a key the CLI assumes it can be found in your environment variables
as 'API_KEY'.

    $ export API_KEY=YOUR_API_KEY

If you wish to apply your credentials in a different manner you can modify 
the source code; for example you could hard-code your key into the ReedClient 
object when it is instantiated.

## Basic functionality

The CLI provides two commands, job_search and job_desc.

### job_search

The first function performs a job search using the Reed API. The results are printed 
out in the terminal with a small number of basic job details. 

    $ python reed-cli.py job_search --query='data scientist'

The job search can be narrowed down by providing additional arguments; the
options provided are currently query, num_jobs, days and location.

#### job_desc

This function prints out the full job description of the job with a given job_id,
along with the url for the job entry on the Reed website.

    $ python reed-cli.py job_desc --job_id=12345

Help pages for both functions can be easily called in familar click fashion.

    $ python reed-cli.py job_desc --help
