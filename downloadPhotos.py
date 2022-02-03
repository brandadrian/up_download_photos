import time
import webbrowser
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import datetime

url = 'https://www.uzepatscher.ch/wp-admin/admin.php?page=wppa_admin_menu&album-page-no=1'
downloadBasePath = os.path.join(
    "C:\\uzepatscher\\", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '\\'


def start():
    options = webdriver.ChromeOptions()
    # Headless mode runs chrome in background
    # options.add_argument('headless')
    # Window size must be set for id recognition in headless mode
    options.add_argument('window-size=1920x1080')
    browser = webdriver.Chrome(options=options)
    os.mkdir(downloadBasePath)
    login(browser, url)
    iterateAlbum(browser)


def login(browser, url):
    print("Login to", url)
    browser.get(url)
    time.sleep(2)

    input_username = browser.find_element(By.ID, 'user_login')
    input_password = browser.find_element(By.ID, 'user_pass')
    button_login = browser.find_element(By.ID, 'wp-submit')

    input_username.send_keys('admin')
    input_password.send_keys('uzepatsc')

    button_login.click()

    time.sleep(2)
    print("Login done!")


def iterateAlbum(browser):
    print("Start iterating over albums of", url)
    numberRows = len(browser.find_elements(By.TAG_NAME, 'tr'))

    for rowNumber in range(numberRows):
        if (rowNumber == 0):
            continue

        try:
            row = browser.find_elements(By.TAG_NAME, 'tr')[rowNumber]
            cols = row.find_elements(By.TAG_NAME, 'td')
            id = cols[0].text

            if (id.isdigit()):
                name = cols[1].text
                saison = cols[5].text
                linkToAlbum = cols[7]
                folderName = saison.replace(
                    " ", "_") + '_' + name.replace(" ", "_")
                print("Processing folder: " + folderName)
                linkToAlbum.click()
                time.sleep(5)
                pictureUrls = []
                albumUrl = browser.current_url
                for page in range(1, 10):
                    try:

                        currentUrl = albumUrl + '&wppa-page=' + str(page)
                        print(currentUrl)
                        browser.get(currentUrl)
                        links = browser.find_elements(By.TAG_NAME, 'a')

                        try:
                            for link in links:
                                if ("https://www.uzepatscher.ch/wp-content/uploads/wppa" in link.text and "https://www.uzepatscher.ch/wp-content/uploads/wppa/thumbs" not in link.text):
                                    pictureUrls.append(link.text)
                        finally:
                            downloadPictures(folderName, pictureUrls)
                    except Exception:
                        pass
        finally:
            print("Processed " + str(rowNumber) + " of " + str(numberRows))
            time.sleep(2)
            browser.get(url)
            time.sleep(2)


def downloadPictures(folderName, pictureUrls):
    distinctedPictureUrls = list(set(pictureUrls))
    path = downloadBasePath + folderName
    print("Download", str(len(distinctedPictureUrls)),
          "files to destination ", path)

    if not os.path.exists(path):
        os.mkdir(path)

    for pictureUrl in distinctedPictureUrls:
        r = requests.get(pictureUrl, allow_redirects=True)
        fileName = pictureUrl.split('/')[-1]
        fileLocation = path + '\\' + fileName
        open(fileLocation, 'wb').write(r.content)


start()
