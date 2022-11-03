# import grequests
# from bs4 import BeautifulSoup
# import requests
# from time import time

# ORIGN = f"https://khamsat.com"
# URL = ORIGN +"/community/requests"
# HEADERS = ({'User-Agent':
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
#             (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
#             'Accept-Language': 'en-US, en;q=0.5'})

# urls = [
#     'http://www.heroku.com',
#     'http://tablib.org',
#     'http://httpbin.org',
#     'http://python-requests.org',
#     'http://kennethreitz.com'
# ]
# # rs = (grequests.get(u) for u in urls)
# # final_res = grequests.map(rs)
# # print(final_res)

# def getLinksKhamsast() -> list:
#     links_khamsat = []
#     basePage = requests.get(URL, headers= HEADERS)
#     baseSoup = BeautifulSoup(basePage.text, "lxml")
#     results = baseSoup.findAll(name='tr', attrs={"class" : "forum_post"})
#     for res in results:
#         url = ORIGN + res.find('h3', attrs={"class" : "details-head"}).find('a').get_attribute_list('href')[0]
#         links_khamsat.append(url)
#     return links_khamsat

# def startScrapKhamsat():
#     start = time()
#     links = getLinksKhamsast()
#     # links = links[0:10]
#     rs = (grequests.get(link, headers= HEADERS) for link in links)
#     listResponsceLinks = grequests.map(rs, stream=True)
#     listData = fetchKhamsat(listResponsceLinks)
#     end = time()
#     print(f"time : {end - start}")
#     return listData


# def fetchKhamsat(listRespons) -> list:
#     listOffers = []
#     for res in listRespons:
#         listOffers.append(taskScrapLinksKhamsat(res))
#     return listOffers


# def taskScrapLinksKhamsat(response):
#     myDict = {}
#     soup = BeautifulSoup(response.text, "lxml")
#     content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
#     content = " ".join(content.split())
#     number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
#     publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
#     statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
#     dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]
#     myDict = {"dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher , "content" : content , "number_of_offers" : number_of_offers}
#     return myDict


# startScrapKhamsat()

url = "https://kafiil.com/kafiil/public/project/2821-%D9%85%D8%B5%D9%85%D9%85-%D8%BA%D8%B1%D9%81-%D9%82%D9%8A%D9%85%D9%86%D9%82"
print(url.__contains__("kafiil.com"))