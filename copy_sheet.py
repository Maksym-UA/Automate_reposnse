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

time = strftime("%Y-%m-%d %H:%M", gmtime())
print('\nCurrent time: ', time)

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
    ]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'AutomateAnswer-da18077c9092.json', scope)

service = discovery.build('sheets', 'v4', credentials=credentials)

# The spreadsheet to apply the updates to.
spreadsheet_id = '1bLxxxDHt_73z1P69fuwE'  # TODO: Update placeholder value.

# The ID of the sheet to copy.
sheet_id = '7434xxxx05'  # TODO: Update placeholder value.

copy_sheet_to_another_spreadsheet_request_body = {
    # The ID of the spreadsheet to copy the sheet to.
    'destination_spreadsheet_id': '1bLs3msIlwu8ZsHNmxxxxxxxzrDHt_73z1P69fuwE',
    }

request = service.spreadsheets().sheets().copyTo(
    spreadsheetId=spreadsheet_id, sheetId=sheet_id,
    body=copy_sheet_to_another_spreadsheet_request_body,)

response = request.execute()
print('\n\tName of sheet copied')
print(response['title'])
pprint(response)
