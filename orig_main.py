from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from airtable import Airtable
import time as t
import requests
import sys

try:
    airtable = Airtable('app9sfGVyhyxORMnQ', 'Integromat_apps 01.09', api_key='keyHfCAyvjHyZhzev')
    integromat_apps = []
    for entry in airtable.get_all(view='Grid view'):
        integromat_apps.append(entry['fields']['app_title'])
        
    airtable = Airtable('appsZAkPyGMx1tXqm', 'Zapier_Posts', api_key='keyHfCAyvjHyZhzev')

    url = "https://zapier.com/app/login"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    t.sleep(3)

    driver.find_element_by_xpath('//input[@class="text-input login-form__input"]').send_keys('') # send_keys('Login Email-address')
    driver.find_element_by_xpath('//button/span/span/span[text()="Continue"]').click()
    t.sleep(3)
    driver.find_element_by_xpath('//input[@class="text-input login-form__input"]').send_keys('') # send_keys('Login Password')
    driver.find_element_by_xpath('//button/span/span/span[text()="Continue"]').click()
    t.sleep(3)

    # open zapier community page
    driver.get('https://community.zapier.com/ask-the-community-3')
    t.sleep(3)
    login = driver.find_element_by_xpath('//a[text()="Login"]').get_attribute("href")
    driver.get(login)

    # iterate through all sites
    for i in range(1,6):
        driver.get('https://community.zapier.com/ask-the-community-3/index' + str(i) +'.html')
        t.sleep(3)

        try:
            driver.find_element_by_xpath('//a[text()="Accept cookies"]').click()
        except:
            pass
        
        #get all posts on 1 site
        posts = driver.find_elements_by_xpath('//div[contains(@class, "qa-topic-block topic-view js-thread js-thread-id-")]')
        
        for post in posts:
            header = post.find_element_by_xpath('.//h4/a')
            link = header.get_attribute('href')       
            post_id = link.split('-')[-1]
            header = header.text
            content = post.find_element_by_xpath('.//p/a').text
            
            contains_integromat_app = 0
            keyword = '0'
            for app in integromat_apps:
                if app.casefold() in header.casefold() or app.casefold() in content.casefold():
                    if app.casefold() == "Zapier":
                        continue
                    contains_integromat_app = 1
                    keyword = app
                    break
            airtable.insert({'_post_id': post_id,
                            'link': link,
                            'header': header,
                            'content': content,
                            '_contains_integromat_app': contains_integromat_app,
                            'keyword': keyword,
                            '_reminder_send': 0
                                })
            likes_count_before = post.find_element_by_xpath('.//button/span').text
            post.find_element_by_xpath('.//button').click()
            likes_count_after = post.find_element_by_xpath('.//button/span').text
            if int(likes_count_after) < int(likes_count_before):
                post.find_element_by_xpath('.//button').click()

    requests.get('https://hook.integromat.com/knlwhv4s6kk162r6uv4cmq5rvl8f22em?status=run')
    driver.close()
except:
    requests.get('https://hook.integromat.com/knlwhv4s6kk162r6uv4cmq5rvl8f22em?status=' + str(sys.exc_info()[0]))
    driver.close()