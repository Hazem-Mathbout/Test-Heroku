# # from bs4 import BeautifulSoup
# # from lxml import etree
# # import requests
# # import json
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # import json
# # import time as Ti
# # import os
# # from bs4 import BeautifulSoup
# # import requests
# # from webdriver_manager.chrome import ChromeDriverManager
# # from selenium.webdriver.chrome.service import Service 
# # # url = f'https://khamsat.com/community/requests/600958-%D8%AA%D8%B9%D8%AF%D9%8A%D9%84-%D8%B9%D9%84%D9%89-%D9%85%D9%88%D9%82%D8%B9-%D9%88%D8%B1%D8%AF%D8%A8%D8%B1%D9%8A%D8%B3'
# # # # url = 'https://www.google.com/'
# # # page = requests.get(url)
# # # print(page)
# # # soup = BeautifulSoup(page.content, "html.parser")
# # # # results = soup.find("a", attrs={"class" : "sidebar_user"})
# # # print(soup.prettify())

# # chrome_options = webdriver.ChromeOptions()
# # # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# # chrome_options.add_argument("--window-size=1920,1080")
# # chrome_options.add_argument("--disable-extensions")
# # chrome_options.add_argument("--proxy-server='direct://'")
# # chrome_options.add_argument("--proxy-bypass-list=*")
# # chrome_options.add_argument("--start-maximized")
# # chrome_options.add_argument('--headless')
# # chrome_options.add_argument('--disable-gpu')
# # chrome_options.add_argument('--disable-dev-shm-usage')
# # chrome_options.add_argument('--no-sandbox')
# # chrome_options.add_argument('--ignore-certificate-errors')
# # chrome_options.add_argument('--allow-running-insecure-content')
# # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
# # chrome_options.add_argument(f'user-agent={user_agent}')

# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , chrome_options=chrome_options)
# # # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# # driver.implicitly_wait(10)
# # driver.maximize_window()
# # url = f'https://khamsat.com/community/requests/600958-%D8%AA%D8%B9%D8%AF%D9%8A%D9%84-%D8%B9%D9%84%D9%89-%D9%85%D9%88%D9%82%D8%B9-%D9%88%D8%B1%D8%AF%D8%A8%D8%B1%D9%8A%D8%B3'

# # # url = 'https://khamsat.com/community/requests'
# # driver.get(url)
# # listResult = []
# # results_1 = driver.find_elements(by= By.CLASS_NAME ,value= "details-td.avatar-td__small-padding")
# # numberOfOffers = driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div/div[2]/div/div[3]/div[2]/div[3]/div[1]/h3').text
# # content = driver.find_element(by=By.CLASS_NAME, value='replace_urls').text
# # print(content)
# # publisher = ""
# # statusOfPublisher = ""
# # for res in results_1:
# #     # print(res.text)                      
# #     publisher = res.find_element(by= By.XPATH, value= './h3').text
# #     statusOfPublisher = res.find_element(by=By.XPATH, value= './ul').text
# #     # url = res.find_element(by= By.XPATH, value= './td[2]/h3/a').get_attribute('href')
# #     # time = res.find_element(by=By.XPATH, value= './td[2]/ul/li[2]/span').text
# #     print(statusOfPublisher)
                             
# #     # listResult.append({"webSiteName" : "خمسات" , "title" : title , "" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : None , "url_img" : url_img})
# # # for res in listResult:
# # #     finalRes.update(res)

# # from cgitb import text


# # URL = f"https://kafiil.com/kafiil/public/project/678-%D9%83%D8%AA%D8%A7%D8%A8%D8%A9-%D9%85%D8%AD%D8%AA%D9%88%D9%89-%D8%B9%D9%84%D9%89-%D9%85%D9%88%D9%82%D8%B9-%D9%88%D9%88%D8%B1%D8%AF%D8%A8%D8%B1%D9%8A%D8%B3-%D8%A8%D8%A7%D9%84%D9%84%D8%BA%D8%A9-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"

# HEADERS = ({'User-Agent':
# 			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
# 			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
# 			'Accept-Language': 'en-US, en;q=0.5'})

# # webpage = requests.get(URL, headers=HEADERS)
# # soup = BeautifulSoup(webpage.content, "html.parser")

# # content = soup.find(name= 'p' , attrs={"class" : ""}).text
# # content = " ".join(content.split())
# # number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
# # publisher = soup.find(name='div' , attrs={"class" : "user-info-row"}).find('div').find('a').text
# # publisher = " ".join(publisher.split())
# # statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text
# # status = soup.find(name='bdi', attrs={"class" : "label label-prj-open"}).text
# # price = soup.find(name='span', attrs={"dir" : "rtl"}).text
# # url_img = soup.find(name='div' , attrs={"class" : "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
# # dateTime = soup.find(name= 'span', attrs={"data-toggle" : "tooltip"}).get_attribute_list('title')[0]
# # print(dateTime)



# # import os
# # import redis
# # from rq import Worker, Queue, Connection
# # from greeting import scrapKhamsat

# # listen = ['high', 'default', 'low']

# # redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

# # conn = redis.from_url(redis_url)

# # if __name__ == '__main__':
# #     print("=============")
# #     with Connection(conn):
# #         worker = Worker(map(Queue, listen))
# #         worker.work()
# #         conn.close()


# # ORIGN = f"https://khamsat.com"
# # URL = "https://khamsat.com/ajax/load_more/community/requests"

# # data = "posts_ids%5B%5D=603969&posts_ids%5B%5D=603964&posts_ids%5B%5D=603957&posts_ids%5B%5D=603871&posts_ids%5B%5D=603697&posts_ids%5B%5D=603941&posts_ids%5B%5D=603965&posts_ids%5B%5D=603875&posts_ids%5B%5D=603849&posts_ids%5B%5D=603968&posts_ids%5B%5D=603959&posts_ids%5B%5D=603928&posts_ids%5B%5D=603919&posts_ids%5B%5D=603660&posts_ids%5B%5D=603951&posts_ids%5B%5D=602372&posts_ids%5B%5D=603972&posts_ids%5B%5D=603741&posts_ids%5B%5D=603447&posts_ids%5B%5D=603966&posts_ids%5B%5D=603930&posts_ids%5B%5D=603967&posts_ids%5B%5D=603730&posts_ids%5B%5D=603794&posts_ids%5B%5D=603958&posts_ids%5B%5D=603818&posts_ids%5B%5D=603735&posts_ids%5B%5D=603942&posts_ids%5B%5D=603764&posts_ids%5B%5D=603956&posts_ids%5B%5D=603920&posts_ids%5B%5D=603947&posts_ids%5B%5D=603948&posts_ids%5B%5D=603895&posts_ids%5B%5D=603883&posts_ids%5B%5D=603454&posts_ids%5B%5D=603520&posts_ids%5B%5D=603955&posts_ids%5B%5D=603679&posts_ids%5B%5D=603725&posts_ids%5B%5D=603699&posts_ids%5B%5D=603690&posts_ids%5B%5D=603650&posts_ids%5B%5D=603933&posts_ids%5B%5D=603932&posts_ids%5B%5D=603851&posts_ids%5B%5D=603275&posts_ids%5B%5D=603777&posts_ids%5B%5D=603187&posts_ids%5B%5D=603766"

# # URL = "https://test-api-hroku.herokuapp.com/resLoadMoreKhamsat"


# # response = requests.post(URL, headers=HEADERS, data={"data" : data})
# # print(response)
# # body = response.json()
# # htmlString = body["content"] # string type
# # soup = BeautifulSoup(htmlString, "html.parser")
# # results = soup.findAll(name='tr', attrs={"class" : "forum_post"})

# # res = results[0].find('h3', attrs={"class" : "details-head"}).find('a').get_attribute_list('href')[0]
# # # res = res.split('-')[0].split('/')[-1]
# # print(res)


# # .get_attribute_list('src')[0]

# # u = " "
# # u.split()
# # for res in results:

# # 	img = results[0].find('img').get_attribute_list('src')[0]
# #   url = results[0].findAll('a')[1].get_attribute_list('href')[0]
# #   title = results[0].findAll('a')[1].text
# #   time = results[0].findAll('span')[1].text.strip()
# #   status = results[0].findAll('span')[0].text
# #   price = results[0].findAll('p')[0].text.strip()
# #   number_offers = results[0].findAll('span')[2].text.strip()
# # 	print(title)

# import requests
# import concurrent.futures
# from bs4 import BeautifulSoup
# import json

# ORIGNKHAMSAT = f"https://khamsat.com"
# URLKAMSAT = ORIGNKHAMSAT +"/community/requests"
# URLMOSTAQL = "https://mostaql.com/projects"
# URLKAFIIL = "https://kafiil.com/kafiil/public/projects?page=1&source=web"
# URLS = [URLKAMSAT,
#         URLKAFIIL,
#         URLMOSTAQL,]


# list = "/resLoadMoreKhamsat"
# if "/resLoadMoreKhamsat" in list:
#     print("founded")
# else:
#     print("Not Founded!")

# def scrapKhamsat():
#     ORIGN = f"https://khamsat.com"
#     URL = ORIGN +"/community/requests"
#     # output = request.get_json()

#     finalRes = {}
#     listResult = []
#     basePage = requests.get(URL, headers=HEADERS)
#     baseSoup = BeautifulSoup(basePage.content, "html.parser")

#     results = baseSoup.findAll(name='tr', attrs={"class" : "forum_post"})
#     for i, res in enumerate(results):
#         try:
#              title = res.find('h3', attrs={"class" : "details-head"}).find('a').text
#              url = ORIGN + res.find('h3', attrs={"class" : "details-head"}).find('a').get_attribute_list('href')[0]
#              time = res.find('td', attrs={"class" : "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
#              url_img = res.find('td', attrs={"class" : "avatar-td text-center"}).find('img').get_attribute_list('src')[0]
#              postId = res.get('id').replace("forum_post-", "posts_ids%5B%5D=")


#              # ####################################

#              webpage2 = requests.get(url, headers= HEADERS)
#              soup = BeautifulSoup(webpage2.content, "html.parser")
#              content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
#              content = " ".join(content.split())
#              number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
#              publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
#              statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
#              dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]

#              #####################################

#              listResult.append({"postId" :postId , "dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher ,  "webSiteName" : "khamsat" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : number_of_offers , "url_img" : url_img})
#         except Exception as exp:
#             print(f"This Exception From khamsat one offer {i} the error is : {exc} ")
#     # for res in listResult:
#     #     finalRes.update(res)
#     finalRes = json.dumps(listResult)
#     print(f"finish khamsat here! =>  {len(listResult)}")
#     return (finalRes)

 
# def scrapmostaql():
#     # output = request.get_json()
#     # budget_max = 10000 if output["budget_max"]=="None" else output["budget_max"]
#     # budget_min = 0.00  if output["budget_min"]=="None" else output["budget_min"]
#     # num_bage   = 1     if output["num_bage"]=="None" else output["num_bage"]
#     # category = output["category"]

#     finalRes = {}
#     listResult = []
    
    
#     URL = URLMOSTAQL
#     sourcPage = requests.get(URL, headers=HEADERS)
#     sourcSoup = BeautifulSoup(sourcPage.content, "html.parser")
#     tempRes = sourcSoup.findAll(name='tr', attrs={"class" : "project-row"})
#     if(len(tempRes) != 0):
#         for res in tempRes:
#             try:

#                 title = res.find('a').text
#                 url = res.find('a').get_attribute_list('href')[0]
#                 time = res.find('time').text.strip()
#                 time = "".join(time.split())  
#                 number_of_offers = res.find('ul').findAll('li')[2].text.strip()
#                 postId = url.split('-')[0].split('/')[-1]
#                 ########################################################
#                 webpage2 = requests.get(url, headers= HEADERS)
#                 soup = BeautifulSoup(webpage2.content, "html.parser")
#                 content = soup.find(name= 'div' , attrs={"class" : "text-wrapper-div carda__content"}).text
#                 content = " ".join(content.split())
#                 publisher = soup.find(name='h5' , attrs={"class" : "postcard__title profile__name mrg--an"}).find(name='bdi').text
#                 status = soup.find(name='bdi', attrs={"class" : "label label-prj-open"}).text
#                 price = soup.find(name='span', attrs={"dir" : "rtl"}).text
#                 url_img = soup.find(name='div' , attrs={"class" : "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
#                 dateTime = soup.find(name= 'td', attrs={"data-type" : "project-date"}).find(name='time').get_attribute_list('datetime')[0]
#                 ########################################################          

#                 listResult.append({"postId" : postId , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "mostaql" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
#             except Exception as exc:
#                 print(f"This Exception From mostaql one offer the error is : {exc} ")
#     print(f"finish mostaql here! =>  {len(listResult)}")
#     finalRes = json.dumps(listResult)
#     return (finalRes)
    


# def scrapkafiil():
#     # output = json.loads(request.data, strict = False)
#     # num_bage   = 1 if output["num_bage"]=="None" else output["num_bage"]
#     # category = output["category"]

#     finalRes = {}
#     listResult = []
    
   
   
#     URL = URLKAFIIL
#     sourcPage = requests.get(URL, headers=HEADERS)    
#     sourcSoup = BeautifulSoup(sourcPage.content, "html.parser")
#     tempRes = sourcSoup.findAll(name='div', attrs={"class" : "project-box active"})
#     if len(tempRes) != 0 :
#             for res in tempRes: 
#                 title = res.findAll('a')[1].text.split()
#                 if(title[0] != "قيد"):
#                     title = " ".join(title[1:])
#                 else:
#                     title=" ".join(title[2:])
#                 url = res.findAll('a')[1].get_attribute_list('href')[0]
#                 time = res.findAll('span')[1].text.strip()
#                 status = res.findAll('span')[0].text
#                 price = res.findAll('p')[0].text.strip()
#                 number_of_offers = res.findAll('span')[2].text.strip()
#                 url_img = res.find('img').get_attribute_list('src')[0]
#                 postId = url.split('-')[0].split('/')[-1]
#                 #################################################
#                 webpage2 = requests.get(url, headers= HEADERS)
#                 soup = BeautifulSoup(webpage2.content, "html.parser")
#                 content = soup.find(name= 'p' , attrs={"class" : ""}).text
#                 content = " ".join(content.split())
#                 publisher = soup.find(name='div' , attrs={"class" : "user-info-row"}).find('div').find('a').text
#                 publisher = " ".join(publisher.split())
#                 dateTime = soup.find(name= 'span', attrs={"data-toggle" : "tooltip"}).get_attribute_list('title')[0]
#                 #################################################
#                 listResult.append({"postId" : postId  , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "kafiil" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
         
#     print(f"finish kafiil here! =>  {len(listResult)}")
#     finalRes = json.dumps(listResult)
#     return (finalRes)

# LISTSCRAPING = [scrapKhamsat, scrapkafiil,scrapmostaql]
# print("fifnish here")
# # def load_url(url, timeout):
# #     with requests.get(url, timeout=timeout) as page:
# #         return BeautifulSoup(page.content, "html.parser")
# allData = []
# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#     # Start the load operations and mark each future with its URL
    
#     future_to_website = {executor.submit(website): website for website in LISTSCRAPING}
#     for future in concurrent.futures.as_completed(future_to_website):
#         website = future_to_website[future]
#         try:
#             data = future.result()
#         except Exception as exc:
#             print('%r generated an exception: %s' % (website, exc))
#         else:
#             output = json.loads(data)
#             allData.extend(output)
#             # print('%r page is %d bytes' % (url, len(data)))
#     print(allData)
#     print(f"finish all offer here! =>  {len(allData)}")
#     print(type(allData))


from difflib import SequenceMatcher

# title = "طلب مقالات حصرية عن مسلسل"
# content = ''' 
# السلام عليكم
# اريد 8 ملخصات حصرية عن مسلسلات تركية تم عرض منها الحلقة الاولى.
# (600 كلمة)
# '''

# searchTerm = "مقالاتت"
# listContent = content.split()
# listTitle = title.split()
# if any(searchTerm in word for word in listTitle) :
#     print("Match Found!")
# else :
#     print("Not Found")

# fullstring = "مطلوب محرر فيديو مونتير"
# substring =   ""


# string1 = "I am a test string"
# string2 = "I am a testing string"

# # match = textdistance.cosine(fullstring, substring)
# match =  SequenceMatcher(None, fullstring, substring)
# print(match.ratio())
# print()

list1 = [2,3,4]
list2 = []
list2 = list1
print(list2)