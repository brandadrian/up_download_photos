import time
import webbrowser
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

def start():
    options = webdriver.ChromeOptions()
    #Headless mode runs chrome in background
    #options.add_argument('headless')
    #Window size must be set for id recognition in headless mode
    options.add_argument('window-size=1920x1080') 
    browser = webdriver.Chrome(options=options)
    url = 'https://www.uzepatscher.ch/wp-admin/admin.php?page=wppa_admin_menu&album-page-no=1'

    login(browser, url)

def login(browser, url):
    print("login")
    browser.get(url)

    input_username = browser.find_element(By.ID, 'user_login')
    input_password = browser.find_element(By.ID, 'user_pass')
    button_login = browser.find_element(By.ID, 'wp-submit')
      
    input_username.send_keys('admin')
    input_password.send_keys('uzepatsc')
        
    button_login.click()

    time.sleep(2)
    iterateAlbum(browser)

    ######Iterate pages
    time.sleep(10)

def iterateAlbum(browser):
    numberRows = len(browser.find_elements(By.TAG_NAME, 'tr'))

    for rowNumber in range(numberRows):
        if (rowNumber == 0):
            continue
        
        try:
            row = browser.find_elements(By.TAG_NAME, 'tr')[rowNumber]

            cols = row.find_elements(By.TAG_NAME, 'td')
            id = cols[0].text
            name = cols[1].text
            saison = cols[5].text
            linkToAlbum = cols[7]
            if (id.isdigit()):
                fileName = saison + '_' + name
                print("*********************************")
                print("Processing: " + fileName)
                print("*********************************")
                linkToAlbum.click()
                time.sleep(5)

                links = browser.find_elements(By.TAG_NAME, 'a')
                pictures = []
                try:
                    for link in links:
                        if ("https://www.uzepatscher.ch/wp-content/uploads/wppa" in link.text and "https://www.uzepatscher.ch/wp-content/uploads/wppa/thumbs" not in link.text):
                            pictures.append(link.text)
                finally:
                    print(list(set(pictures)))
        finally:
            print("Processed " + str(rowNumber) + " of " + str(numberRows))
            time.sleep(5)
            browser.back()
            time.sleep(2)

start()