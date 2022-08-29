from attr import attr
from bs4 import BeautifulSoup
from lxml import etree
import requests




# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import json
# import time as Ti
# import os
# from bs4 import BeautifulSoup
# import requests
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service 
# # url = f'https://khamsat.com/community/requests/600958-%D8%AA%D8%B9%D8%AF%D9%8A%D9%84-%D8%B9%D9%84%D9%89-%D9%85%D9%88%D9%82%D8%B9-%D9%88%D8%B1%D8%AF%D8%A8%D8%B1%D9%8A%D8%B3'
# # # url = 'https://www.google.com/'
# # page = requests.get(url)
# # print(page)
# # soup = BeautifulSoup(page.content, "html.parser")
# # # results = soup.find("a", attrs={"class" : "sidebar_user"})
# # print(soup.prettify())

# chrome_options = webdriver.ChromeOptions()
# # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--proxy-server='direct://'")
# chrome_options.add_argument("--proxy-bypass-list=*")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--allow-running-insecure-content')
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
# chrome_options.add_argument(f'user-agent={user_agent}')

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , chrome_options=chrome_options)
# # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# driver.implicitly_wait(10)
# driver.maximize_window()
# url = f'https://khamsat.com/community/requests/600958-%D8%AA%D8%B9%D8%AF%D9%8A%D9%84-%D8%B9%D9%84%D9%89-%D9%85%D9%88%D9%82%D8%B9-%D9%88%D8%B1%D8%AF%D8%A8%D8%B1%D9%8A%D8%B3'

# # url = 'https://khamsat.com/community/requests'
# driver.get(url)
# listResult = []
# results_1 = driver.find_elements(by= By.CLASS_NAME ,value= "details-td.avatar-td__small-padding")
# numberOfOffers = driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div/div[2]/div/div[3]/div[2]/div[3]/div[1]/h3').text
# content = driver.find_element(by=By.CLASS_NAME, value='replace_urls').text
# print(content)
# publisher = ""
# statusOfPublisher = ""
# for res in results_1:
#     # print(res.text)                      
#     publisher = res.find_element(by= By.XPATH, value= './h3').text
#     statusOfPublisher = res.find_element(by=By.XPATH, value= './ul').text
#     # url = res.find_element(by= By.XPATH, value= './td[2]/h3/a').get_attribute('href')
#     # time = res.find_element(by=By.XPATH, value= './td[2]/ul/li[2]/span').text
#     print(statusOfPublisher)
                             
#     # listResult.append({"webSiteName" : "خمسات" , "title" : title , "" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : None , "url_img" : url_img})
# # for res in listResult:
# #     finalRes.update(res)

# from cgitb import text


URL = f"https://kafiil.com/kafiil/public/project/678-%D9%83%D8%AA%D8%A7%D8%A8%D8%A9-%D9%85%D8%AD%D8%AA%D9%88%D9%89-%D8%B9%D9%84%D9%89-%D9%85%D9%88%D9%82%D8%B9-%D9%88%D9%88%D8%B1%D8%AF%D8%A8%D8%B1%D9%8A%D8%B3-%D8%A8%D8%A7%D9%84%D9%84%D8%BA%D8%A9-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"

HEADERS = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
			'Accept-Language': 'en-US, en;q=0.5'})

# webpage = requests.get(URL, headers=HEADERS)
# soup = BeautifulSoup(webpage.content, "html.parser")

# content = soup.find(name= 'p' , attrs={"class" : ""}).text
# content = " ".join(content.split())
# number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
# publisher = soup.find(name='div' , attrs={"class" : "user-info-row"}).find('div').find('a').text
# publisher = " ".join(publisher.split())
# statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text
# status = soup.find(name='bdi', attrs={"class" : "label label-prj-open"}).text
# price = soup.find(name='span', attrs={"dir" : "rtl"}).text
# url_img = soup.find(name='div' , attrs={"class" : "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
# dateTime = soup.find(name= 'span', attrs={"data-toggle" : "tooltip"}).get_attribute_list('title')[0]
# print(dateTime)



# import os
# import redis
# from rq import Worker, Queue, Connection
# from greeting import scrapKhamsat

# listen = ['high', 'default', 'low']

# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

# conn = redis.from_url(redis_url)

# if __name__ == '__main__':
#     print("=============")
#     with Connection(conn):
#         worker = Worker(map(Queue, listen))
#         worker.work()
#         conn.close()


# ORIGN = f"https://khamsat.com"
URL = "https://mostaql.com/projects"
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
results = soup.findAll(name='tr', attrs={"class" : "project-row"})
res = results[0].find('time').text.strip()
res = "".join(res.split())
print(res)


# .get_attribute_list('src')[0]

# u = " "
# u.split()
# for res in results:

# 	img = results[0].find('img').get_attribute_list('src')[0]
#   url = results[0].findAll('a')[1].get_attribute_list('href')[0]
#   title = results[0].findAll('a')[1].text
#   time = results[0].findAll('span')[1].text.strip()
#   status = results[0].findAll('span')[0].text
#   price = results[0].findAll('p')[0].text.strip()
#   number_offers = results[0].findAll('span')[2].text.strip()
# 	print(title)