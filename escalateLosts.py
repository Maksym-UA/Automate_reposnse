# gspread is a Python client library for the Google Sheets API
import unittest
import gspread
import selenium.webdriver.support.ui as ui
import selenium.webdriver as webdriver
import requests

# This is a Python library for accessing resources protected by OAuth 2.0
from oauth2client.service_account import ServiceAccountCredentials

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
from time import sleep

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']

'''OAuth credentials can be generated in several different ways using the
oauth2client library provided by Google. If you are editing spreadsheets
for yourself then the easiest way to generate credentials is to use Signed
Credentials stored in your application (see example below). If you plan to
edit spreadsheets on behalf of others then visit the Google OAuth2
documentation for more information.'''


creds = ServiceAccountCredentials.from_json_keyfile_name('AutomateAnswer-' +
                                                         'da18077c9092.json',
                                                         scope)

# pass credentials
client = gspread.authorize(creds)

# open working spreadsheet
sheet = client.open('test_for_python')

# switch to current worksheet
worksheet = sheet.worksheet("testForLost")

# worksheet.update_acell('B2', "it's down there somewhere, let me take look.")

# set range of cells to work with
cell_list = worksheet.range('A1:B3')

listOtLinks = []


def allItemsToList():
    i = 0
    for cell in cell_list:
        if 'http' in cell.value:
            listOtLinks.append(cell.value)
            i = i + 1
        # print (listOtLinks)


class EscalateLosts():
    '''
    This class gets links of previously saved tickets on lost items and upon
    verifying information on the load page, closes the ticket( if resolved)
    or escalates it to level 2 support)
    '''

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'D:\chrome' +
                                       'driver.exe')
        self.actions = ActionChains(self.driver)

    def startOneLogin(self):
        self.driver.get('https://uber.onelogin.com/client/apps')

    def loginIn(self):
        '''Log in to onelogin app'''

        try:
            self.elementMail = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'user_email')))

            self.elementPass = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'user_password')))

        except Exception:
            print('Page takes too long to respond')

        finally:
            # send email
            self.driver.find_element_by_id('user_email')
            self.elementMail.clear()
            self.elementMail.send_keys('your_actual_eamil')

            # send password
            self.driver.find_element_by_id('user_password')
            self.elementPass.clear()
            self.elementPass.send_keys('xxxx')
            self.driver.find_element_by_id('user_submit').click()

    def confirmByPush(self):
        try:
            # locate confirmation frame
            self.pressPushButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                r'//*[@id="xxx_iframe"]')))

        except Exception:
            print('No push button found')

        finally:

            # switch to confirmation frame
            self.frame = self.driver.find_element_by_xpath(
                '//*[@id="xxx_iframe"]')
            self.driver.switch_to.frame(self.frame)

            # find push button and click
            self.pressPushButton = self.driver.find_element_by_xpath(
                "//button[contains(., 'Send Me a Push')]").click()
            self.pressPushButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="logo"]/img')))

    def openTicket(self):
        '''Read link and open it in a new tab.'''

        link = 'link to the ticket'

        # link = listOtLinks[0]

        # open link in a new tab and focus on it
        tab = "window.open('" + link + "').focus();"
        self.driver.execute_script(tab)
        # self.driver.get(link) opens in same window

        try:
            self.elem = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/main/div/div[3]')))

        except TimeoutException:
            pass
        finally:
            print('open URL : ' + link)

    def ticketStatus(self):
        '''Check whether contact was reviewed previously.'''

        # get total numbers of windows open
        windows = self.driver.window_handles
        print('\nThese are weblements/objects of windows handles')
        print(windows)

        mainWindow = self.driver.current_window_handle

        # switch to the last opened window
        self.driver.switch_to.window(windows[-1])
        print('\n\tOpened new tab URL - ' + windows[-1])

        try:
            self.elem = self.driver.find_element_by_css_selector(
                'div.conversation-pane')

        except NoSuchElementException:
            print('tired of this, no loading right side. what the hell!')

        finally:
            # if 'solved' or 'awaiting for reply' in self.elem.text.lower():
            # print ('\nTicket already reviewed')

            # else:
            # session.loadContactTypes()
            # session.checkWhoWrote()
            session.loadContactTypes()
            session.checkWhoWrote()
            session.escalateOpenTicketToLevelTwo()
            # close the last window
            # self.driver.close()

            # switch to the initial/main window
            # self.driver.switch_to.window(windows[0])
            # print('\nInitial window: ' + windows[0])

    def loadContactTypes(self):
        '''WAit till contacts get loaded.'''

        try:
            self.elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//*[@id="app"]/div/div/main/div/div[3]/header/div/div' +
                    '/div/span/span')
                ))

        except NoSuchElementException:
            return False

        finally:
            print ('\nContacts successfully loaded')

    def checkWhoWrote(self):
        '''Check who contact originally came from.'''

        try:
            self.elem = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/main/div/div[3]/header')

        except NoSuchElementException:
            print('tired of this, not loading right side. what the hell!')

        finally:
            if 'rider' in self.elem.text.lower():
                print('\n\tUser tells about lost item')
                # call method for user
                session.selectRiderLostItem()
                session.addRidersSavedReply()

            else:
                print('Driver tells about found lost item')
                # call method for driver
                session.selectDriverFoundItem()

    def selectRiderLostItem(self):
        '''Select type for user.'''

        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, '//*[@id="app"]/div/div/main/div/div[3]/' +
                    'header/div/div/div/span'
                )
            )).click()

        # search in tree for 'trouble coordinating'
        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="app"]/div/div/main/div/div[3]/header/div/div' +
                    '/div/span/span[2]/span/div/div/div[3]/div/ul/li[7]/a'
                )))

        if self.elem.text == 'Trouble coordinating to return item':
            print('\ncontact type' + self.elem.get_attribute("innerHTML"))
            # self.elem.click()

        else:
            print('did not find "trouble coordinating" type for rider')

    def addRidersSavedReply(self):
        '''Select saved reply for rider'''

        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="app"]/div/div/main/div/div[3]/div[3]/div[2]/div' +
                '/div/div[2]/ul/li/button'))).click()

        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                 By.XPATH,
                 '//*[@id="app"]/div/div/main/div/div[3]/div[3]/div[2]/div/' +
                 'div/div[2]/ul/li[3]/button'))).click()
        # get the tree of all Lost items category
        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                 By.XPATH, '//*[@id="app"]/div/div/main/div/div[3]/div[3]/' +
                 'div[2]/span/div/ul')))

        # select specified contact type
        li = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/main/div/div[3]/div[3]/div[2]/span/div' +
            '/ul/li/span[contains(text(), "string_here: search_words")]')
        print('\n\tSaved reply button to be pressed inner HTML - ' +
              li.get_attribute("innerHTML"))
        print('\n' + li.text)
        li.click()

        # self.elem = WebDriverWait(self.driver, 5).until(
        # EC.element_to_be_clickable((
        # By.XPATH,'//*[@id="app"]/div/div/main/div/div[3]/div[3]/div[2]/' +
        # 'span/div/ul/li[' + self.replyIndex + ']')))
        # self.elem.click()

    def selectDriverFoundItem(self):
        '''Select type for user.'''

        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="app"]/div/div/main/div/div[3]/header/div/div/' +
                div/span'))).click()

        # search input line for contacts
        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="app"]/div/div/main/div/div[3]/header/div/div/'
                    'div/span/span[2]/span/div/div/div[2]/input')
                )
            )
        print(self.elem.get_attribute("innerHTML"))

        # make sure input is clean
        self.elem.clear()
        print('input field cleaned')

        self.elem.send_keys('Driver found item in vehicle')
        print('\n"Driver found item in vehicle" contact type entered')

        self.elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="app"]/div/div/main/div/div[3]/header/div/div/div' +
                '/span/span[2]/span/div/div/div[3]/div/ul/li/a/div[2]')))
        print('\n' + self.elem.get_attribute('innerHTML'))

        if 'Driver found item in vehicle' in self.elem.text:
            print('\n\t' + self.elem.get_attribute('innerHTML'))
            # self.elem.click()
            print('\n"Driver found item in vehicle" button clicked')

        else:
            print('did not succeed to click "Driver found item in vehicle" ' +
                  'type for driver')

    def escalateOpenTicketToLevelTwo(self):
        '''Escalating tickets to level 2'''

        # find button row with input requested
        self.elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/' +
                                        'main/div/div[3]/div[3]/div[2]/' +
                                        'div[2]/div/button[2]/i'))).click()

        # find button for 'additional information'
        self.elem = WebDriverWait(self.driver, 10).until(
           EC.element_to_be_clickable((
               By.XPATH, '//*[@id="app"]/div/div/' +
               'main/div/div[3]/div[3]/div[2]/div/div[2]/div/ul/li[2]/' +
               'span'))).click()
        print('\n\tAdditional information button pressed')

        # find button to unselect reply field
        self.elem = WebDriverWait(self.driver, 10).until(
           EC.element_to_be_clickable((
               By.XPATH, '//*[@id="app"]/div/div/' +
               'main/div/div[3]/div[3]/div[2]/div[2]/div/button/i')))
        print('\nReply field can be toggled off')

        # find button row with open, awaiting, solved
        self.sendButtons = self.driver.find_element_by_css_selector(
            'ul.btn-group')

        # find 'open' button and click
        self.openButton = self.driver.find_element_by_xpath(
            '//ul[@class="btn-group"]/li/button').click()

        print('\n\tOpen button pressed')

        # click again to confirm
        # self.sendButtons.click()
        # print('confirmation button pressed')
        # self.driver.implicitly_wait(5)


session = EscalateLosts()
allItemsToList()
session.startOneLogin()
session.loginIn()
session.confirmByPush()
session.openTicket()
session.ticketStatus()

if __name__ == '__main__':
    print (EscalateLosts.__doc__)
