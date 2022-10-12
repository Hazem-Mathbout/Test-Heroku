import json
from time import time
from bs4 import BeautifulSoup
import requests
import concurrent.futures
from difflib import SequenceMatcher
import textdistance
# from multiprocessing import Process, Lock
from flask import Flask, request, jsonify


app = Flask(__name__)

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /getmsg/?name=
    name = request.args.get("name", None)

    # For debugging
    print(f"Received: {name}")

    response = {}

    # Check if the user sent a name at all
    if not name:
        response["ERROR"] = "No name found. Please send a name."
    # Check if the user entered a number
    elif str(name).isdigit():
        response["ERROR"] = "The name can't be numeric. Please send a string."
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome API!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome API!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "No name found. Please send a name."
        })
 


 

@app.route("/resKham", methods = ["POST" , "GET"])
def scrapKhamsat(requests_session = None ,output = None):
    start_time = time()
    ORIGN = f"https://khamsat.com"
    URL = ORIGN +"/community/requests"
    payloadForSearchTerm = ""  
    listResult = []
    templistResult = []
    try:
        if output == None:
            requests_session = requests.Session()
        basePage = requests_session.get(URL, headers=HEADERS)
        baseSoup = BeautifulSoup(basePage.text, "lxml")
        results = baseSoup.findAll(name='tr', attrs={"class" : "forum_post"})
        if(len(results) != 0):
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                future_to_offer = {executor.submit(taskKahmsatScraping, offer): offer for offer in results}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        templistResult.append(data)
            # with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
                future_to_offer = {executor.submit(taskScrapLinksKhamsat, offer , requests_session): offer for offer in templistResult}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        print("***************************************************")
                        print(data)
                        payloadForSearchTerm = payloadForSearchTerm + data["postId"] + "&"
                        listResult.append(data)

        listResult.append({"all_post_id" : payloadForSearchTerm})

        print(f"Number Offers: {len(listResult)}")
        # requests_session.close()
        print(f"{(time() - start_time):.2f} seconds")
    except Exception as exc:
        pass
        print(f"This Exception When Connect To Khamsat error is : {exc}") 
    if output != None:
        finalRes = json.dumps(listResult)
        return (finalRes)
    else:
        # requests_session.close()   
        return jsonify(listResult)



def getMorOfferMatchSearchTerm(payloadSearch = None , searchTerm = None, listResult = list) -> list:
    URL = "https://khamsat.com/ajax/load_more/community/requests"
    ORIGN = f"https://khamsat.com"
    searchTerm = searchTerm
    dataLoadMore = payloadSearch
    listResult = listResult
    try:
         response = requests.post(URL, headers=HEADERS, data=dataLoadMore.removesuffix('&'))
         body = response.json()
         htmlString = body["content"]
         sourcSoup = BeautifulSoup(htmlString, "html.parser")
         results = sourcSoup.findAll(name='tr', attrs={"class" : "forum_post"})
    except Exception as exc:
         print(f"This Exception When Connect To Load More Buttom Khamsat the error is : {exc}")
    for i, res in enumerate(results):
        try:
             title = res.find('h3', attrs={"class" : "details-head"}).find('a').text
             url = ORIGN + res.find('h3', attrs={"class" : "details-head"}).find('a').get_attribute_list('href')[0]
             time = res.find('td', attrs={"class" : "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
             url_img = res.find('td', attrs={"class" : "avatar-td text-center"}).find('img').get_attribute_list('src')[0]
             postId = res.get('id').replace("forum_post-", "posts_ids%5B%5D=")
            

             webpage2 = requests.get(url, headers= HEADERS)
             soup = BeautifulSoup(webpage2.content, "html.parser")
             content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
             content = " ".join(content.split())
              # ####################################
             dataLoadMore = dataLoadMore + postId + "&"
             if searchTerm.strip() != "" :
                    check_result = checkOfferForSearchTerm(searchTerm=searchTerm ,title=title, content=content)
                    if check_result == False:
                        continue
             # ####################################
             number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
             publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
             statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
             dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]

             #####################################

             listResult.append({"postId" :postId , "dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher ,  "webSiteName" : "khamsat" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : number_of_offers , "url_img" : url_img})
        except Exception as exc:
            print(f"This Exception From read More Khamsat get offer  the error is : {exc}")
    
    listResult.append({"all_post_id" : dataLoadMore})
    print(f"Number of post id for all offer Now is: {len(dataLoadMore.split('&'))}")
    return listResult

 
@app.route("/resMost", methods = ["POST" , "GET"])
def scrapmostaql(requests_session = None ,output = None):
    isFuncInternal = False
    if output == None:
        requests_session = requests.Session()
        try:
             output = request.get_json()
        except Exception as exc:
            pass
            print(f"generated an exception when convert to json in route /resMost =>: {exc}") 
            print(f"The output Now in /resMost is: {output}")
    else :
        isFuncInternal = True
    budget_max = 10000 if output["budget_max"]=="None" else output["budget_max"]
    budget_min = 0.00  if output["budget_min"]=="None" else output["budget_min"]
    num_bage_mostaql   = 1     if output["num_bage_mostaql"]=="None" or 0 else output["num_bage_mostaql"]
    category_mostaql = output["category_mostaql"]
    delivery_duration_for_mostaql = "" if output["delivery_duration_for_mostaql"]=="None" else output["delivery_duration_for_mostaql"]
    skills_for_mostaql = output["skills_for_mostaql"]
    searchTerm = output["searchTerm"]

    # finalRes = {}
    listResult = []
    
    if category_mostaql == "None" : 
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&keyword={searchTerm}&skills={skills_for_mostaql}&duration={delivery_duration_for_mostaql.removesuffix(',')}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    else:
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&keyword={searchTerm}&category={category_mostaql}&skills={skills_for_mostaql}&duration={delivery_duration_for_mostaql.removesuffix(',')}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    try:
        sourcPage = requests_session.get(URL, headers=HEADERS)
        sourcSoup = BeautifulSoup(sourcPage.text, "lxml")
        tempRes = sourcSoup.findAll(name='tr', attrs={"class" : "project-row"})
        if(len(tempRes) != 0):
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                future_to_offer = {executor.submit(taskScrapMostaql, offer, requests_session): offer for offer in tempRes}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        print("***************************************************")
                        print(data)
                        listResult.append(data)
                    #  listResult.append({"postId" : postId , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "mostaql" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
        print(f'Number Offer mostaql is: {len(listResult)}')
        requests_session.close()
    except Exception as exc:
        print(f"This Exception When Connect to Mostaql the error is : {exc}")
    if isFuncInternal:
        finalRes = json.dumps(listResult)
        return (finalRes)
    else:
        return jsonify(listResult)
    


@app.route("/resKafi", methods = ["POST" , "GET"])
def scrapkafiil(requests_session = None,output = None):
    isFuncInternal = False
    if output == None:
        requests_session = requests.Session()
        try:
            # output = json.loads(request.data, strict = False)
            output = request.get_json()
        except Exception as exc:
            pass
            print(f"generated an exception when convert to json in route /resKafi => : {exc}") 
    else:
        isFuncInternal = True
    num_bage_kafiil   = 1 if output["num_bage_kafiil"]=="None" or 0 else output["num_bage_kafiil"]
    category_kafiil = output["category_kafiil"]
    delivery_duration_for_kafiil = "" if output["delivery_duration_for_kafiil"]=="None" else output["delivery_duration_for_kafiil"]
    budget_max = 10000 if output["budget_max"]=="None" else output["budget_max"]
    budget_min = 0.00  if output["budget_min"]=="None" else output["budget_min"]
    searchTerm = output["searchTerm"]

    listResult = []
    
    if category_kafiil == "None" : 
        URL = f"https://kafiil.com/kafiil/public/projects?delivery_duration={delivery_duration_for_kafiil.removesuffix(',')}&page={num_bage_kafiil}&search={searchTerm}&source=web"
    else:
        URL = f"https://kafiil.com/kafiil/public/projects/{category_kafiil}?delivery_duration={delivery_duration_for_kafiil.removesuffix(',')}&page={num_bage_kafiil}&search={searchTerm}&source=web"
    try:
         sourcPage = requests_session.get(URL, headers=HEADERS)    
         sourcSoup = BeautifulSoup(sourcPage.text, "lxml")
         tempRes = sourcSoup.findAll(name='div', attrs={"class" : "project-box active"})
         if len(tempRes) != 0 :
             with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                future_to_offer = {executor.submit(taskScrapKafiil, offer, requests_session, budget_min, budget_max): offer for offer in tempRes}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        print("***************************************************")
                        print(data)
                        listResult.append(data)
         print(f"Number offers in kafiil {len(listResult)}")
         requests_session.close()
    except Exception as exc:
         print(f"This Exception When connect To Kafiil the error is : {exc}")

    if isFuncInternal:
        finalRes = json.dumps(listResult)
        return (finalRes)
    else:
        return jsonify(listResult)


@app.route("/resLoadMoreKhamsat", methods = ["POST", "GET"])
def scrapKhamsatLoadMore(requests_session= None ,output = None):
    isFuncInternal = False
    dataLoadMore = ""
    templistResult = []
    listResult = []
    if output == None:
        requests_session = requests.Session()
        try:
            output = request.get_json()
        except Exception as exc:
            print(f"generated an exception when convert to json in route /resLoadMoreKhamsat => : {exc}") 
    else:
        isFuncInternal = True
    URL = "https://khamsat.com/ajax/load_more/community/requests"
    ORIGN = f"https://khamsat.com"
    try:
         dataLoadMore   = output["dataLoadMore"]
        #  searchTerm = output["searchTerm"]
         response = requests_session.post(URL, headers=HEADERS, data=dataLoadMore.removesuffix('&'))
         if response.status_code == 200 or response.status_code == 201:
             body = response.json()
             htmlString = body["content"]
             sourcSoup = BeautifulSoup(htmlString, "lxml")
             results = sourcSoup.findAll(name='tr', attrs={"class" : "forum_post"})
         else:
             return jsonify(["error"])
    except Exception as exc:
        print(f"Exception When connect to khmasta load more ... the error is: {exc}")
  
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_offer = {executor.submit(taskKahmsatScraping, offer): offer for offer in results}
            for future in concurrent.futures.as_completed(future_to_offer):
                offer = future_to_offer[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (offer, exc))
                else:
                    templistResult.append(data)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            future_to_offer = {executor.submit(taskScrapLinksKhamsat, offer , requests_session): offer for offer in templistResult}
            for future in concurrent.futures.as_completed(future_to_offer):
                offer = future_to_offer[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (offer, exc))
                else:
                    print("***************************************************")
                    print(data)
                    dataLoadMore = dataLoadMore + data["postId"] + "&"
                    listResult.append(data)

    except Exception as exc:
         print(f"This Exception When read More Khamsat get offer the error is : {exc}")

    listResult.append({"all_post_id" : dataLoadMore})
    if isFuncInternal:
        finalRes = json.dumps(listResult)
        return (finalRes)
    else:
        requests_session.close()
        return jsonify(listResult)




@app.route('/searchKhamsat', methods = ["POST", "GET"])
def searchKhamsat():
    requests_session = requests.Session()
    allData = []
    dataLoadMore = None
    total_num_page = 0
    try:
        output = request.get_json()
        dataLoadMore   = output["dataLoadMore"]
        total_num_page = output["total_num_page"]
        if dataLoadMore != None and dataLoadMore != "":
            for _ in range(total_num_page):
                data = scrapKhamsatLoadMore(requests_session ,output= output)
                data_object = json.loads(data)
                lastElement = data_object.pop()
                initDataLoadMore =  output["dataLoadMore"] + lastElement["all_post_id"]
                output["dataLoadMore"] = initDataLoadMore
                allData.extend(data_object)

        else:
            data = scrapKhamsat(requests_session ,output= 'Internal Func Excuction')
            data_object = json.loads(data)
            lastElement = data_object.pop()
            initDataLoadMore = lastElement["all_post_id"]
            allData.extend(data_object)        
            output = {"dataLoadMore" : initDataLoadMore}
            for _ in range(total_num_page - 1):
                data = scrapKhamsatLoadMore(requests_session ,output= output)
                data_object = json.loads(data)
                lastElement = data_object.pop()
                initDataLoadMore = output["dataLoadMore"] +  lastElement["all_post_id"]
                output["dataLoadMore"] = initDataLoadMore
                allData.extend(data_object)
    except Exception as exc:
        print(f"generated an exception in searchKhamsat => : {exc}")
    print(f"========== Number of List Search is : {len(allData)}")
    requests_session.close()
    return jsonify(allData)


def removeUnSpportWebSiteForSearching(list_website, searchTerm):
    List_Not_Support_Searching = [scrapKhamsat, scrapKhamsatLoadMore]
    if searchTerm != "":
        for website in list_website:
            for websiteNotSupportSearch in List_Not_Support_Searching:
                if websiteNotSupportSearch == website:
                    list_website.remove(websiteNotSupportSearch)
    return list_website


@app.route('/home', methods = ["POST", "GET"])
def offersForHome():
    requests_session = requests.Session()
    allData = []
    payload = json.loads(request.data, strict = False)
    postedData   = payload["route"]
    if "/resLoadMoreKhamsat" in postedData:
        LISTSCRAPING = [scrapkafiil, scrapKhamsatLoadMore, scrapmostaql]
    else:
        LISTSCRAPING = [scrapKhamsat, scrapkafiil,scrapmostaql]
 
    NEW_LIST_SCRAPING = removeUnSpportWebSiteForSearching(LISTSCRAPING, payload["searchTerm"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_website = {executor.submit(website, requests_session, payload): website for website in NEW_LIST_SCRAPING}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (website, exc))
            else:
                print("***************************************************")
                output = json.loads(data)
                allData.extend(output)
    # finalRes = json.dumps(allData)
    print(len(allData))
    requests_session.close()
    return jsonify(allData)


def checkOfferForSearchTerm(searchTerm : str ,title : str, content:str) :
   match1 =  SequenceMatcher(None, searchTerm, title)
   match2 =  SequenceMatcher(None, searchTerm, content)
   for el in searchTerm.split():
       if(el in title or el in content):
           return True
   if(match1.ratio() >= 0.5 or match2.ratio() >= 0.5):
       return True
   if(textdistance.cosine(searchTerm, title) >= 0.5):
       return True
   else:
       return False 

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"




def taskKahmsatScraping(res) -> dict:
    myDict = {}
    ORIGN = f"https://khamsat.com"
    URL = ORIGN +"/community/requests"
    try:
         title = res.find('h3', attrs={"class" : "details-head"}).find('a').text
         url = ORIGN + res.find('h3', attrs={"class" : "details-head"}).find('a').get_attribute_list('href')[0]
         time = res.find('td', attrs={"class" : "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
         url_img = res.find('td', attrs={"class" : "avatar-td text-center"}).find('img').get_attribute_list('src')[0]
         postId = res.get('id').replace("forum_post-", "posts_ids%5B%5D=")

         # ####################################

        #  webpage2 = requests_session.get(url, headers= HEADERS)
        #  soup = BeautifulSoup(webpage2.text, "lxml")
        #  content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
        #  content = " ".join(content.split())
        #  ##################
        # #  payloadForSearchTerm = payloadForSearchTerm + postId + "&"
        #  ##################
        #  number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
        #  publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
        #  statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
        #  dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]
        #  myDict = {"postId" :postId , "dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher ,  "webSiteName" : "khamsat" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : number_of_offers , "url_img" : url_img}
         myDict = {"postId" :postId ,   "webSiteName" : "khamsat" , "title" : title ,  "url" : url , "time" : time , "status" : None , "price" : None ,  "url_img" : url_img}
    except Exception as exc:
         print(f"This Exception From khamsat get offer the error is : {exc}")
    return myDict


def taskScrapLinksKhamsat(offer,requests_session):
         myDict = {}
         webpage2 = requests_session.get(offer["url"], headers= HEADERS)
         soup = BeautifulSoup(webpage2.text, "lxml")
         content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
         content = " ".join(content.split())
         number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
         publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
         statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
         dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]
         myDict = {"dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher , "content" : content , "number_of_offers" : number_of_offers}
         offer.update(myDict)
         return offer


def taskScrapMostaql(res, requests_session) -> dict:
    myDict = {}
    try:
        title = res.find('a').text
        url = res.find('a').get_attribute_list('href')[0]
        time = res.find('time').text.strip()
        time = "".join(time.split())  
        number_of_offers = res.find('ul').findAll('li')[2].text.strip()
        postId = url.split('-')[0].split('/')[-1]
        ########################################################
        webpage2 = requests_session.get(url, headers= HEADERS)
        soup = BeautifulSoup(webpage2.text, "lxml")
        content = soup.find(name= 'div' , attrs={"class" : "text-wrapper-div carda__content"}).text
        content = " ".join(content.split())
        publisher = soup.find(name='h5' , attrs={"class" : "postcard__title profile__name mrg--an"}).find(name='bdi').text
        status = soup.find(name='bdi', attrs={"class" : "label label-prj-open"}).text
        price = soup.find(name='span', attrs={"dir" : "rtl"}).text
        url_img = soup.find(name='div' , attrs={"class" : "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
        dateTime = soup.find(name= 'td', attrs={"data-type" : "project-date"}).find(name='time').get_attribute_list('datetime')[0]
        ########################################################
        myDict = {"postId" : postId , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "mostaql" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img}
    except Exception as exc:
        print(f"This Exception From mostaql get offer the error is : {exc}")
    return myDict

def taskScrapKafiil(res, requests_session,budget_min,budget_max) -> dict:
    myDict = {}
    price = res.findAll('p')[0].text.strip()
    list_price = price.split('-')
    numMin = int(list_price[0].strip().removeprefix('$'))
    numMax = int(list_price[1].strip().removeprefix('$'))
    budget_max = int(float(budget_max))
    budget_min = int(float(budget_min))
    if((budget_min > 0 or budget_max < 10000) and  not(numMin >= budget_min and numMax <= budget_max)):
        return
    try:
         title = res.findAll('a')[1].text.split()
         if(title[0] != "قيد"):
             title = " ".join(title[1:])
         else:
             title=" ".join(title[2:])
         url = res.findAll('a')[1].get_attribute_list('href')[0]
         time = res.findAll('span')[1].text.strip()
         status = res.findAll('span')[0].text
         number_of_offers = res.findAll('span')[2].text.strip()
         url_img = res.find('img').get_attribute_list('src')[0]
         postId = url.split('-')[0].split('/')[-1]
         #################################################
         webpage2 = requests_session.get(url, headers= HEADERS)
         soup = BeautifulSoup(webpage2.text, "lxml")
         content = soup.find(name= 'p' , attrs={"class" : ""}).text
         content = " ".join(content.split())
         publisher = soup.find(name='div' , attrs={"class" : "user-info-row"}).find('div').find('a').text
         publisher = " ".join(publisher.split())
         dateTime = soup.find(name= 'span', attrs={"data-toggle" : "tooltip"}).get_attribute_list('title')[0]
         myDict = {"postId" : postId  , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "kafiil" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img}
    except Exception as exc:
         print(f"This Exception From kafiil get offer the error is : {exc}")
    return myDict    

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)