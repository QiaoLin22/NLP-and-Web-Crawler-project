import html2text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from requests import get
import lxml.html
import re
from IPython.core.display import clear_output
from time import time
from time import sleep
from random import randint
from fake_useragent import UserAgent
from itertools import cycle
from urllib.request import Request, urlopen
ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]
proxies_req = Request('https://www.sslproxies.org/')
proxies_req.add_header('User-Agent', ua.random)
proxies_doc = urlopen(proxies_req).read().decode('utf8')
ipsoup = BeautifulSoup(proxies_doc, 'html.parser')
proxies_table = ipsoup.find(id='proxylisttable')

# Save proxies in the array
for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
    'ip':
    row.find_all('td')[0].string,
    'port': row.find_all('td')[1].string
  })
proxy_pool = cycle(proxies)
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
def find(driver):
    element = driver.find_elements_by_id("mat-input-0")
    if element:
        return element
    else:
        return False
pd_url=pd.read_csv('C:/Users/Administrator/Desktop/WebScraping/curnchbase download/IT companies info.csv')
url_list=list(pd_url['Organization Name URL'])

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome()  # chrome_options=options, executable_path=r'C:/Users/Administrator/Desktop/WebScraping/chromedriver')
driver.maximize_window()
# driver.get('https://www.crunchbase.com/search/organization.companies/66e2f8bf5573fb73efb20c4ba2a512a0') #the url you want


# initial the colunms you want(list type)
# df_master=pd.DataFrame()
name = []
descrption = []
funding_date = []
funding_type = []
contact_email = []
contact_phone = []

count = 0
for url in url_list:

    count += 1
    print(url)

    if count % 100 == 0:
        driver.close()

        proxy = next(proxy_pool)
        print(proxy)
        # driver.close()
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--proxy-server = ' + str(proxy))
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()

    driver.get(url)
    sleep(randint(2, 3))

    if check_exists_by_xpath('//*[@id="px-captcha"]') is True:
        print("Block page appear")
        element2 = driver.find_element_by_xpath('//*[@id="px-captcha"]')
        ActionChains(driver).move_to_element(element2).perform()
        ActionChains(driver).move_by_offset(-500, 0).perform()
        ActionChains(driver).click_and_hold().perform()
        sleep(5)
        ActionChains(driver).release().perform()

    if check_exists_by_xpath(
            '/html/body/chrome/div/header/mat-toolbar[1]/span[3]/session-controls/div/a[1]/span') is True:

        try:
            myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-input-0')))
            print("Page is ready!")
        except TimeoutException:
            print('Loading took too much time!')

        login = driver.find_element_by_xpath(
            "//html/body/chrome/div/header/mat-toolbar[1]/span[3]/session-controls/div/a[1]/span")
        login.click()

        try:
            elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-input-2')))
            print("Page is ready!")
        except TimeoutException:
            print('Loading took too much time!')

        username = driver.find_element_by_id("mat-input-1")
        password = driver.find_element_by_id("mat-input-2")

        username.send_keys("sophia.dou@zgccapital.com")
        password.send_keys("zgcpass2015")

        driver.find_element_by_css_selector("[type=submit]").click()
        sleep(randint(2, 3))

    # name
    try:
        titles_elements = driver.find_elements_by_xpath(
            """//*[@id="section-overview"]/mat-card/div[2]/image-with-fields-card/image-with-text-card/div/div/div[2]/div[1]""")[
            0]
        title = titles_elements.text
        name.append(title)
    except:
        continue

    # Description
    if check_exists_by_xpath("""//*[@id="section-overview"]/mat-card/div[2]/description-card/div""") is True:
        try:
            rm = driver.find_element_by_link_text("Read More")
            if rm.is_displayed():
                rm.click()  # this will click the element if it is there
                print("FOUND THE LINK CREATE ACTIVITY! and Clicked it!")
                desp_elements = \
                driver.find_elements_by_xpath("""//*[@id="section-overview"]/mat-card/div[2]/description-card/div""")[0]
                desp = desp_elements.text
                descrption.append(desp)

        except NoSuchElementException:
            print("...")
            desp_elements = \
            driver.find_elements_by_xpath("""//*[@id="section-overview"]/mat-card/div[2]/description-card/div""")[0]
            desp = desp_elements.text
            descrption.append(desp)
    else:
        desp = "None"
        descrption.append(desp)
        # sleep(randint(1,2))

    # funding date
    if check_exists_by_xpath(
            "//span[@class='component--field-formatter field-type-date_precision ng-star-inserted']") is True:
        funding_elements = driver.find_elements_by_xpath(
            "//span[@class='component--field-formatter field-type-date_precision ng-star-inserted']")[0]
        funding = funding_elements.text
        funding_date.append(funding)
    else:
        funding = "None"
        funding_date.append(funding)

    # funding type
    if check_exists_by_xpath("//a[contains(@href, 'last_funding_type')]") is True:
        funding_type_elements = driver.find_elements_by_xpath("//a[contains(@href, 'last_funding_type')]")[0]
        f_type = funding_type_elements.text
        funding_type.append(f_type)
    else:
        f_type = "None"
        funding_type.append(f_type)

    # contact_info_email & phone number  can be used

    if check_exists_by_xpath("//span[contains(text(),'@')]") is True:
        contact_elements = driver.find_elements_by_xpath("//span[contains(text(),'@')]")[0]
        contact_1 = contact_elements.text
        contact_email.append(contact_1)
    else:
        contact_1 = "None"
        contact_email.append(contact_1)

    # some problem to locate the phone number
    # str2 = "<>(111)111-1111</><>1(111)111-1111</><>+11111111111</><>111-111-1111</>"
    doc = driver.page_source
    phone_type1 = re.compile(r">([(][\d]{3}[)][\d]{3}-[\d]{4})<").findall(doc)
    phone_type2 = re.compile(r">([\d][(][\d]{3}[)][\d]{3}-[\d]{4})<").findall(doc)
    phone_type3 = re.compile(r">([\d]{10})<").findall(doc)
    phone_type4 = re.compile(r">(\+[\d]{11})<").findall(doc)
    phone_type5 = re.compile(r">([\d]{3}-[\d]{3}-[\d]{4})<").findall(doc)
    phone_type6 = re.compile(r">([(][\d]{3}[)]\s[\d]{3}-[\d]{4})<").findall(doc)
    phone = (phone_type1 + phone_type2 + phone_type3 + phone_type4 + phone_type5 + phone_type6)
    if len(phone) == 0:
        phone_1 = "None"
    else:
        phone_1 = phone[0]
    contact_phone.append(phone_1)

    print(count)

df=pd.DataFrame()
df["name"]=name
df["descrption"]=descrption
df["funding date"]=funding_date
df["funding type"]=funding_type
df["email"]=contact_email
df["phone number"]=contact_phone
df.to_csv("wudi_IT.csv")
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome('/Users/mycomputer/Desktop/web/chromedriver')#chrome_options=options, executable_path=r'C:/Users/Administrator/Desktop/WebScraping/chromedriver')
driver.maximize_window()
driver.get('https://www.crunchbase.com/organization/epic-games-2#section-locked-charts') #the url you want

try:
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-input-0')))
    print( "Page is ready!")
except TimeoutException:
    print('Loading took too much time!')


if check_exists_by_xpath("//span[contains(text(), 'CEO')]" or "[contains(text(), 'Chief Executive Officer')]") is True:
    print('CEO founded')
    ceo_elements = driver.find_element_by_xpath("//span[contains(text(), 'CEO')]/../../..a[1]")
    print(ceo_elements)
    ceo_p1 = ceo_elements.find_element_by_xpath('..')
    ceo = ceo_p1.text
else:
    print('No CEO')
    ceo = 'none'