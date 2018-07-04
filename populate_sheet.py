# gspread is a Python client library for the Google Sheets API
import gspread

# This is a Python library for accessing resources protected by OAuth 2.0
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

'''OAuth credentials can be generated in several different ways using the
oauth2client library provided by Google. If you are editing spreadsheets
for yourself then the easiest way to generate credentials is to use Signed
Credentials stored in your application (see example below). If you plan to
edit spreadsheets on behalf of others then visit the Google OAuth2
documentation for more information.'''
creds = ServiceAccountCredentials.from_json_keyfile_name('AutomateAnswer-' +
                                                         'da18077c9092.json',
                                                         scope)
client = gspread.authorize(creds)

sheet = client.open('test_for_python').sheet1

'''this is to test insert and delete rows of cells in spreadsheets but that
turns to be too slow, especially with many rows (>100)

#sheet.insert_row(['This',  'is', 'a', 'test', '30', '5', '2018'], 2)
#for i in range( 4):
#    sheet.delete_row(i+1)'''

# set range to be used in spredsheet to save memory
cellsToUpdate = sheet.range('A1:E8')

# initiate a test list. Eventually it will be populated with customers data
my_list_of_lists = [['This', 'is', 'a ', 'new', 'run'],
                    ['using', 'bigger', 'strings', 'and', 'it'],
                    ['still', 'works', 'fine.', 'Tried', 'to'],
                    ['add', 'long', 'URL', 'like', 'this'],
                    ['http://gspread.readthedocs.io/en/latest/oauth2.html',
                     '99999999', 'and ', 'still', 'OK'],
                    ['Hope', 'it', 'stays ', 'the same', 'with'],
                    ['much', 'bigger', 'files!!!', 'dfgfdgdfffffff',
                     'looks good:)'], ['now ', 'it', 'updates', 'much',
                    'faster']]
# -----------------------------------------------------------------------------

# create empty list to hold all values
total_list = []


def AllItemsToList():
    '''This function saves all items of nested lists to one list.

    >>> total_list = []
    >>> list = [['This','is','a ','new','run'],
                    ['using','bigger','strings','and','it']]
    >>>AllItemsToList()
    >>>print (total_list)
    ['This','is','a ','new','run','using','bigger','strings','and','it']
    '''
    for i in my_list_of_lists:
        for k in i:
            total_list.append(k)
    # print (total_list)


def UpdateDefinedCells():
    '''This function updates cells in an earlier defined range of cells in
    a Google spreadsheet.
    >>> UpdateDefinedCells()
    '''
    i = 0

    for cell in cellsToUpdate:
        cell.value = total_list[i]
        # print(cell.value)
        i = i + 1

    '''update works really fast comparing to insert'''
    sheet.update_cells(cellsToUpdate)

AllItemsToList()
UpdateDefinedCells()
notes = sheet.get_all_records()
print(notes)
