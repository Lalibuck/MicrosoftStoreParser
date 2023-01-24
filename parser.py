import os
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def driver_preprocess():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    return browser


def category_parser(browser, amount=200, category='Business'):
    """Microsoft Store category page parser and forming list of application page links"""
    # preprocessing a category page link
    link = 'https://apps.microsoft.com/store/category/' + category.replace(' ', '%20')
    # get category page by selenium
    browser.get(link)
    # app link xpath
    xpath_link = '//*[@id="all-products-listall-list-container"]/div/div[{}]/div/a'
    # app links list
    links_list = []
    for i in range(1, amount + 1):
        try:
            # find element
            browser.find_element(By.XPATH, xpath_link.format(i))
        except NoSuchElementException:
            # scroll down if element isn't displayed
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # waiting until loading elements
            WebDriverWait(browser, 20).until(ec.presence_of_element_located((By.XPATH, xpath_link.format(i))))
        element = browser.find_element(By.XPATH, xpath_link.format(i))
        # get app link
        links_list.append(element.get_attribute('href'))
    return links_list


def page_parser(browser, link):
    """Microsoft Store application page parser and retrieving name, company, release year and email"""
    # get application page by selenium
    browser.get(link)
    # app name xpath
    name_xpath = '//div[@id="main"]/div/div/div/div/div/div/h1'
    # company name element xpath
    company_xpath = '//div[@id="main"]/div/div/div/div/div/div/a'
    # release year element xpath
    release_xpath = '//*[@id="main"]/div/div/div[1]/div[3]/div[2]/div/div[1]/span/div/span'
    # company e-mail element xpath
    mail_xpath = '//a[contains(@href, "mailto:")]'
    # avoiding reloading and redirecting
    while True:
        try:
            # waiting until loading elements
            WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.XPATH, name_xpath)))
            break
        except TimeoutException:
            browser.get(link)
    # avoiding stale elements
    while True:
        try:
            browser.find_element(By.XPATH, name_xpath)
            browser.find_element(By.XPATH, company_xpath)
            browser.find_element(By.XPATH, release_xpath).get_attribute('innerHTML')
            browser.find_element(By.ID, 'contactInfoButton_desktop')
            break
        except NoSuchElementException:
            break
        except StaleElementReferenceException:
            browser.get(link)
    # app name
    name = browser.find_element(By.XPATH, name_xpath)
    # company name
    company = browser.find_element(By.XPATH, company_xpath)
    # check existing and retrieving release year element
    try:
        browser.find_element(By.XPATH, release_xpath).get_attribute('innerHTML')
    except NoSuchElementException:
        release = ''
    else:
        release = browser.find_element(By.XPATH, release_xpath).get_attribute('innerHTML')
        release = release[27:]
    # check existing and retrieving company e-mail element
    try:
        # find and click contact information element
        browser.find_element(By.ID, 'contactInfoButton_desktop').click()
        browser.find_element(By.XPATH, mail_xpath)
    except NoSuchElementException:
        mail = ''
    else:
        mail = browser.find_element(By.XPATH, mail_xpath)
        mail = mail.text
    return name.text, company.text, release, mail
