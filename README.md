# Volume Scan

## To run:
 * [Install and launch docker](https://docs.docker.com/install/)
 * [Install Python 3](https://www.python.org/downloads/)
 * [Install pip 3](https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3)
 * Run command: `pip install datetime simplejson couchdb requests tabulate`
 * Run command: `docker run -d -p 5984:5984 -v ~/couchdb/data --name couchdb apache/couchdb:1.7.1`
 * To start data polling, run: `python poll.py`
 * To display volume changes, run `python display.py`

#### To make poll use an alternate conig file:
 * `python poll.py -c=configLocation.json`

#### To make display sort by volumes at 15 minutes, descending:
 * `python display.py 15 -r`
 
#### To make display sort by volumes at 30 minutes, ascending, and use config options from alternate location:
 * `python display.py 30 -c=configLocation.json`
 
#### Config options:
 * _**intervalsInMinutes:**_ Array of times to show (In minutes)
 * _**midMarketCapThreshold:**_ Minimum market cap to have symbol/market cap displayed in yellow
 * _**largeMarketCapThreshold:**_ Minimum market cap to have symbol/market cap displayed in green
 * _**symbolsToDisplay:**_ Array of symbols to show (If empty all symbols are shown)
 * _**pollInternvalInSeconds:**_ How frequently to poll for/refresh data
 * _**volChangeFormatThresholds:**_ Array of numbers dictating how to color cells:
    * _**Red:**_ below 1st number
    * _**Yellow:**_ below 2nd 
    * _**Light Blue:**_ above 3rd
    * _**Green:**_ above 4th
    * _**Blue:**_ if none of above conditions met








