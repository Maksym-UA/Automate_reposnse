"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""

from time import gmtime, strftime, time
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from googleapiclient import discovery
from apiclient.discovery import build

# TODO: Change placeholder below to generate authentication credentials. See
# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
#
# Authorize using one of the following scopes:
#     'https://www.googleapis.com/auth/drive'
#     'https://www.googleapis.com/auth/drive.file'
#     'https://www.googleapis.com/auth/spreadsheets'

time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print('Current time: ', time)

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
    ]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'AutomateAnswer-da18077c9092.json',
    scope)

service = discovery.build('sheets', 'v4', credentials=credentials)

# The spreadsheet to apply the updates to.
spreadsheet_id = '1wu8ZsHxxxxnzrDHt_73uwE'  # TODO: Update placeholder value.


requests = []
requests.append({
    'duplicateSheet': {
        # select sheet you want to duplicate
        'sourceSheetId': '743xxxx205',

        # set index you want your sheet to appear
        'insertSheetIndex': '2',
        'newSheetName': '%s' % time
    }
})
body = {
    'requests': requests
}

response = service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body=body).execute()

# TODO: Change code below to process the `response` dict:
pprint(response)
