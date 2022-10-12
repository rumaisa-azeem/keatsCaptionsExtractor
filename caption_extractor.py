from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities#
import json
import time
from selenium.webdriver.common.by import By
from parser import parseSubs
import webbrowser
import os

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get("https://keats.kcl.ac.uk") #insert own url here

while driver.current_url != 'https://keats.kcl.ac.uk/my/':
    print('waiting for log in')
    time.sleep(5)
print('logged in')
input('navigate to page with video and then hit enter in this console')

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

browser_log = driver.get_log('performance') #log is returned as a list
 
urls = [] 
for i in range (len(browser_log)):
    if 'response' in list(json.loads(browser_log[i]['message'])['message']['params'].keys()):
        urls.append(json.loads(browser_log[i]['message'])['message']['params']['response']['url'])
           
target = False
 
for i in urls:
    if 'multirequest' in i and 'caption' in i:
        target = i
        
        
if target != False:
    driver.get(target)
    url = (driver.find_element(By.TAG_NAME, 'body').get_attribute('innerText'))[2:-2]
    driver.get(url)
    response = driver.find_element(By.TAG_NAME, ('body')).get_attribute('innerText')
    driver.close()
    subFile = open('temp.srt', 'w')
    subFile.write(response)
    subFile.close()
    para = parseSubs('temp.srt')
    output = open('output.txt', 'w')
    output.write(para)
    output.close()
    os.remove('temp.srt')
    webbrowser.open('output.txt')
    
input('extraction complete - hit enter to quit')