import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome(executable_path=r'C:\Users\chromedriver.exe')
driver.get('https://www.google.com/')


def CloseNewTab():
    '''Closes newly opened tab after all manupilations made'''

    link = 'http://sport.ua/'

    # open link in a new tab and focus on it
    tab = "window.open('" + link + "').focus();"
    driver.execute_script(tab)

    sleep(3)

    # get total numbers of windows open
    windows = driver.window_handles
    print(windows)

    mainWindow = driver.current_window_handle

    # switch to the last opened window
    driver.switch_to.window(windows[-1])
    print(windows[-1])

    # close the last window
    driver.close()

    # switch to the initial/main window
    driver.switch_to.window(windows[0])
    print(windows[0])

CloseNewTab()

if __name__ == '__main__':
    print (CloseNewTab.__doc__)


    
