import json
from time import time
from typing import List
from bs4 import BeautifulSoup
import requests
import concurrent.futures
from difflib import SequenceMatcher
import textdistance
# from multiprocessing import Process, Lock
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
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


@app.route("/resKham", methods=["POST", "GET"])
def scrapKhamsat(requests_session=None, output=None):
    isFuncInternal = False
    payloadForSearchTerm = ""
    baseSoup = BeautifulSoup("", 'lxml')
    ORIGN = f"https://khamsat.com"
    URL = ORIGN + "/community/requests"
    URL_LOAD_MORE = "https://khamsat.com/ajax/load_more/community/requests"
    listResult = []
    templistResult = []
    try:
        if output == None:
            requests_session = requests.Session()
            try:
                output = request.get_json()
            except Exception as exc:
                pass
                print(
                    f"generated an exception when convert to json in route /resKham =>: {exc}")
        else:
            isFuncInternal = True

        num_page_khamsat = output["num_page_khamsat"]
        offset = output["offset_khamsat"]
        limit = 25 if output["limit"] > 25 else output["limit"]

        if (num_page_khamsat > 1):
            dataLoadMore = str(output["dataLoadMore"])
            response = requests_session.post(
                URL_LOAD_MORE, headers=HEADERS, data=dataLoadMore.removesuffix('&'))
            print("status code for load more khamsat request is: ",
                  response.status_code)
            if response.status_code == 200 or response.status_code == 201:
                body = response.json()
                htmlString = body["content"]
                baseSoup = BeautifulSoup(htmlString, "lxml")
        else:
            basePage = requests_session.get(URL, headers=HEADERS)
            baseSoup = BeautifulSoup(basePage.text, "lxml")

        results = baseSoup.findAll(name='tr', attrs={"class": "forum_post"})
        results = results[offset: offset+limit]
        if (len(results) != 0):
            with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                future_to_offer = {executor.submit(
                    taskKahmsatScraping, offer): offer for offer in results}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print(
                            '%r generated an exception in route /resKham: %s' % (offer, exc))
                    else:
                        if len(data) != 0:
                            templistResult.append(data)

                future_to_Link_offer = {executor.submit(
                    taskScrapLinksKhamsat, offer, requests_session): offer for offer in templistResult}
                for future in concurrent.futures.as_completed(future_to_Link_offer):
                    offer = future_to_Link_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print(
                            '%r generated an exception in route /resKham: %s' % (offer, exc))
                    else:
                        payloadForSearchTerm = payloadForSearchTerm + \
                            data["postId"] + "&"
                        listResult.append(data)
        try:
            listResult.sort(key=lambda x: x['dateTime'], reverse=True)
        except Exception as exc:
            print(f"Error occure when sorting offers khamsat, error is:{exc}")
        listResult.append({"all_post_id": payloadForSearchTerm})
        print(f"Number Offers in khamsat: {len(listResult)}")
    except Exception as exc:
        pass
        print(f"This Exception When Connect To Khamsat error is : {exc}")
    if isFuncInternal:
        finalRes = json.dumps(listResult)
        return (finalRes)
    else:
        requests_session.close()
        return jsonify(listResult)


def getMorOfferMatchSearchTerm(payloadSearch=None, searchTerm=None, listResult=list) -> list:
    URL = "https://khamsat.com/ajax/load_more/community/requests"
    ORIGN = f"https://khamsat.com"
    searchTerm = searchTerm
    dataLoadMore = payloadSearch
    listResult = listResult
    try:
        response = requests.post(URL, headers=HEADERS,
                                 data=dataLoadMore.removesuffix('&'))
        body = response.json()
        htmlString = body["content"]
        sourcSoup = BeautifulSoup(htmlString, "html.parser")
        results = sourcSoup.findAll(name='tr', attrs={"class": "forum_post"})
    except Exception as exc:
        print(
            f"This Exception When Connect To Load More Buttom Khamsat the error is : {exc}")
    for i, res in enumerate(results):
        try:
            title = res.find(
                'h3', attrs={"class": "details-head"}).find('a').text
            url = ORIGN + \
                res.find('h3', attrs={"class": "details-head"}
                         ).find('a').get_attribute_list('href')[0]
            time = res.find('td', attrs={
                            "class": "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
            url_img = res.find('td', attrs={
                               "class": "avatar-td text-center"}).find('img').get_attribute_list('src')[0]
            postId = res.get('id').replace("forum_post-", "posts_ids%5B%5D=")

            webpage2 = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(webpage2.content, "html.parser")
            content = soup.find(name='article', attrs={
                                "class": "replace_urls"}).text
            content = " ".join(content.split())
            # ####################################
            dataLoadMore = dataLoadMore + postId + "&"
            if searchTerm.strip() != "":
                check_result = checkOfferForSearchTerm(
                    searchTerm=searchTerm, title=title, content=content)
                if check_result == False:
                    continue
            # ####################################
            number_of_offers = soup.findAll(
                name='div', attrs={"class": "card-header bg-white"})[1].find(name='h3').text
            publisher = soup.find(
                name='a', attrs={"class": "sidebar_user"}).text
            statusOfPublisher = soup.find(
                name='ul', attrs={"class": "details-list"}).find(name='li').text.strip()
            dateTime = soup.findAll(name='div', attrs={
                                    "class": "col-6"})[1].find(name='span').get_attribute_list('title')[0]

            #####################################

            listResult.append({"postId": postId, "dateTime": dateTime, "publisher": publisher, "statusOfPublisher": statusOfPublisher,  "webSiteName": "khamsat",
                              "title": title, "content": content, "url": url, "time": time, "status": None, "price": None, "number_of_offers": number_of_offers, "url_img": url_img})
        except Exception as exc:
            print(
                f"This Exception From read More Khamsat get offer  the error is : {exc}")

    listResult.append({"all_post_id": dataLoadMore})
    print(
        f"Number of post id for all offer Now is: {len(dataLoadMore.split('&'))}")
    return listResult


@app.route("/resMost", methods=["POST", "GET"])
def scrapmostaql(requests_session=None, output=None):
    isFuncInternal = False
    if output == None:
        requests_session = requests.Session()
        try:
            output = request.get_json()
        except Exception as exc:
            pass
            print(
                f"generated an exception when convert to json in route /resMost =>: {exc}")
            print(f"The output Now in /resMost is: {output}")
    else:
        isFuncInternal = True
    offset = output["offset_mostaql"]
    limit = 25 if output["limit"] > 25 else output["limit"]
    budget_max = 10000 if output["budget_max"] == "None" else output["budget_max"]
    budget_min = 0.00 if output["budget_min"] == "None" else output["budget_min"]
    num_bage_mostaql = 1 if output["num_bage_mostaql"] == "None" or 0 else output["num_bage_mostaql"]
    category_mostaql = output["category_mostaql"]
    delivery_duration_for_mostaql = "" if output[
        "delivery_duration_for_mostaql"] == "None" else output["delivery_duration_for_mostaql"]
    skills_for_mostaql = output["skills_for_mostaql"]
    searchTerm = output["searchTerm"]

    # finalRes = {}
    listResult = []

    if category_mostaql == "None":
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&keyword={searchTerm}&skills={skills_for_mostaql}&duration={delivery_duration_for_mostaql.removesuffix(',')}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    else:
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&keyword={searchTerm}&category={category_mostaql}&skills={skills_for_mostaql}&duration={delivery_duration_for_mostaql.removesuffix(',')}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    try:
        sourcPage = requests_session.get(URL, headers=HEADERS)
        sourcSoup = BeautifulSoup(sourcPage.text, "lxml")
        tempRes = sourcSoup.findAll(name='tr', attrs={"class": "project-row"})
        tempRes = tempRes[offset: offset+limit]
        if (len(tempRes) != 0):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_offer = {executor.submit(
                    taskScrapMostaql, offer, requests_session): offer for offer in tempRes}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        print("***************************************************")
                        if len(data) != 0:
                            print(data)
                            listResult.append(data)
                    #  listResult.append({"postId" : postId , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "mostaql" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
        print(f'Number Offer mostaql is: {len(listResult)}')
    except Exception as exc:
        print(f"This Exception When Connect to Mostaql the error is : {exc}")
    try:
        listResult.sort(key=lambda x: x['dateTime'], reverse=True)
    except Exception as exc:
        print(f"Error occure when sorting offers mostaql, error is:{exc}")
    if isFuncInternal:
        finalRes = json.dumps(listResult)
        return (finalRes)
    else:
        requests_session.close()
        return jsonify(listResult)


@app.route("/resKafi", methods=["POST", "GET"])
def scrapkafiil(requests_session=None, output=None):
    isFuncInternal = False
    if output == None:
        requests_session = requests.Session()
        try:
            # output = json.loads(request.data, strict = False)
            output = request.get_json()
        except Exception as exc:
            pass
            print(
                f"generated an exception when convert to json in route /resKafi => : {exc}")
    else:
        isFuncInternal = True
    num_bage_kafiil = 1 if output["num_bage_kafiil"] == "None" or 0 else output["num_bage_kafiil"]
    category_kafiil = output["category_kafiil"]
    delivery_duration_for_kafiil = "" if output[
        "delivery_duration_for_kafiil"] == "None" else output["delivery_duration_for_kafiil"]
    budget_max = 10000 if output["budget_max"] == "None" else output["budget_max"]
    budget_min = 0.00 if output["budget_min"] == "None" else output["budget_min"]
    searchTerm = output["searchTerm"]
    offset = output["offset_kafiil"]
    limit = 25 if output["limit"] > 25 else output["limit"]

    listResult = []

    if category_kafiil == "None":
        URL = f"https://kafiil.com/kafiil/public/projects?delivery_duration={delivery_duration_for_kafiil.removesuffix(',')}&page={num_bage_kafiil}&search={searchTerm}&source=web"
    else:
        URL = f"https://kafiil.com/kafiil/public/projects/{category_kafiil}?delivery_duration={delivery_duration_for_kafiil.removesuffix(',')}&page={num_bage_kafiil}&search={searchTerm}&source=web"
    try:
        sourcPage = requests_session.get(URL, headers=HEADERS, )
        sourcSoup = BeautifulSoup(sourcPage.text, "lxml")
        tempRes = sourcSoup.findAll(
            name='div', attrs={"class": "project-box active"})
        tempRes = tempRes[offset: offset+limit]
        if len(tempRes) != 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_offer = {executor.submit(
                    taskScrapKafiil, offer, requests_session, budget_min, budget_max): offer for offer in tempRes}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        print("***************************************************")
                        if len(data) != 0:
                            print(data)
                            listResult.append(data)
        print(f"Number offers in kafiil {len(listResult)}")

    except Exception as exc:
        print(f"This Exception When connect To Kafiil the error is : {exc}")
    try:
        listResult.sort(key=lambda x: x['dateTime'], reverse=True)
    except Exception as axc:
        print(f"Error occure when sorting offers kafiil, error is:{exc}")
    if isFuncInternal:
        finalRes = json.dumps(listResult)
        return (finalRes)
    else:
        requests_session.close()
        return jsonify(listResult)


@app.route('/searchKhamsat', methods=["POST", "GET"])
def searchKhamsat():
    requests_session = requests.Session()
    allData = []
    dataLoadMore = None
    total_num_page = 0
    try:
        output = request.get_json()
        dataLoadMore = "" if output["dataLoadMore"] == None else output["dataLoadMore"]
        total_num_page = output["total_num_page"]
        num_page_khamsat = 1
        offset = 0
        limit = 25
        payload_khamsat = {"dataLoadMore": dataLoadMore,
                           "num_page_khamsat": num_page_khamsat, "offset_khamsat": offset, "limit": limit}
        for _ in range(total_num_page):
            data = scrapKhamsat(requests_session, output=payload_khamsat)
            data_object = json.loads(data)
            lastElement = data_object.pop()
            num_page_khamsat = num_page_khamsat + 1
            payload_khamsat["dataLoadMore"] = payload_khamsat["dataLoadMore"] + \
                lastElement["all_post_id"]
            payload_khamsat["num_page_khamsat"] = num_page_khamsat
            allData.extend(data_object)
    except Exception as exc:
        print(f"generated an exception in searchKhamsat => : {exc}")
    print(f"========== Number of List Search is : {len(allData)}")
    requests_session.close()
    return jsonify(allData)


def removeUnSpportWebSiteForSearching(list_website, searchTerm):
    List_Not_Support_Searching = [scrapKhamsat]
    if searchTerm != "":
        for website in list_website:
            for websiteNotSupportSearch in List_Not_Support_Searching:
                if websiteNotSupportSearch == website:
                    list_website.remove(websiteNotSupportSearch)
    return list_website


@app.route('/home', methods=["POST", "GET"])
def offersForHome():
    requests_session = requests.Session()
    allData = []
    payload = json.loads(request.data, strict=False)
    LISTSCRAPING = [scrapKhamsat, scrapkafiil, scrapmostaql]
    NEW_LIST_SCRAPING = removeUnSpportWebSiteForSearching(
        LISTSCRAPING, payload["searchTerm"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_website = {executor.submit(
            website, requests_session, payload): website for website in NEW_LIST_SCRAPING}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception in route /home: %s' %
                      (website, exc))
            else:
                output = json.loads(data)
                allData.extend(output)
                # try :
                #     allData.sort(key=lambda x: x['dateTime'], reverse=True)
                # except:
                #     print("Key dateTime Not Found!")
    mapAllPostId = [item for item in allData if item.get(
        'all_post_id') != None]
    sortedAllData = [
        item for item in allData if item.get('all_post_id') == None]
    try:
        sortedAllData.sort(key=lambda x: x['dateTime'], reverse=True)
    except Exception as exc:
        print(f"Error occure when sorting offers home, error is:{exc}")
    sortedAllData.extend(mapAllPostId)
    print("number offers in home: ", len(sortedAllData))
    requests_session.close()
    return jsonify(sortedAllData)


@app.route('/notification', methods=["POST", "GET"])
def fetchNotifications():
    requests_session = requests.Session()
    allData = []
    final_Data_Notification = []
    payload = json.loads(request.data, strict=False)
    # notif_day = payload['notif_day']
    notif_hour = payload['notif_hour']
    notif_min = payload['notif_min']
    websiteDisabled = payload['websiteDisabled']
    notif_min = 15  # <-- ovveride notif_min the client option -->
    notif_hour = 0  # <-- ovveride notif_hour the client option -->
    td_client = timedelta(hours=notif_hour, minutes=notif_min)
    # LISTSCRAPING = [scrapKhamsat, scrapkafiil,scrapmostaql]
    LISTSCRAPING = getListScrappingForNotificationa(websiteDisabled)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_website = {executor.submit(
            website, requests_session, payload): website for website in LISTSCRAPING}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception in route /notification: %s' %
                      (website, exc))
            else:
                output = json.loads(data)
                allData.extend(output)
    allData_without_allPostId = [
        item for item in allData if item.get('all_post_id') == None]
    for offer in allData_without_allPostId:
        date_now = datetime.now().utcnow()
        date_offer_string = offer['dateTime']
        date_time_offer_obj = datetime.strptime(
            date_offer_string, '%Y-%m-%d %H:%M:%S')
        td_all_info = date_now - date_time_offer_obj
        days = td_all_info.days
        hours, remainder = divmod(td_all_info.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        td_offer = timedelta(hours=hours, minutes=minutes)
        # print(f"num days:({days}) num hours:({hours}) num minutes:({minutes}) --> ({td_offer}) , ({td_client})")
        if td_client >= td_offer and days == 0:
            final_Data_Notification.append(offer)
    print(
        f"Number Offers in Notification List is: {len(final_Data_Notification)}")
    print(f"website blocked from notification is:{websiteDisabled}")
    requests_session.close()
    return jsonify(final_Data_Notification)


def getListScrappingForNotificationa(listNotAllowed: str) -> List:
    listSCRAPING = [scrapKhamsat, scrapkafiil, scrapmostaql]
    if (listNotAllowed == "" or listNotAllowed == ","):
        return listSCRAPING
    makeListNotAllowed = listNotAllowed.removesuffix(',').split(",")
    for element in makeListNotAllowed:
        if element.__contains__('khamsat'):
            listSCRAPING.remove(scrapKhamsat)
        elif element.__contains__('mostaql'):
            listSCRAPING.remove(scrapmostaql)
        else:
            listSCRAPING.remove(scrapkafiil)
    return listSCRAPING


def checkOfferForSearchTerm(searchTerm: str, title: str, content: str):
    match1 = SequenceMatcher(None, searchTerm, title)
    match2 = SequenceMatcher(None, searchTerm, content)
    for el in searchTerm.split():
        if (el in title or el in content):
            return True
    if (match1.ratio() >= 0.5 or match2.ratio() >= 0.5):
        return True
    if (textdistance.cosine(searchTerm, title) >= 0.5):
        return True
    else:
        return False


@app.route("/updateInfo", methods=["POST", "GET"])
def updateInfo():
    requests_session = requests.Session()
    number_of_offers = None
    payload = json.loads(request.data, strict=False)
    url = str(payload["url"])
    basePage = requests_session.get(url, headers=HEADERS)
    soup = BeautifulSoup(basePage.text, "lxml")
    try:
        if url.__contains__("kafiil.com"):
            number_of_offers = soup.find(name='table', attrs={
                                         "class": "info-table"}).findAll('tr')[3].findAll('td')[1].text.strip()
            number_of_offers = f"التعليقات ({number_of_offers})"
        elif url.__contains__("khamsat.com"):
            number_of_offers = soup.findAll(name='div', attrs={
                                            "class": "card-header bg-white"})[1].find(name='h3').text.strip()
        elif url.__contains__("mostaql.com"):
            number_of_offers = soup.find('table', attrs={
                                         "class": "table table-borderless mrg--an text-meta"}).findAll('tr')[5].findAll('td')[1].text.strip()
            number_of_offers = f"التعليقات ({number_of_offers})"
    except Exception as exc:
        print(
            f"Exception occure when updated info in route /updateInfo, the error is: {exc}")
        pass
    print(number_of_offers)
    requests_session.close()
    return jsonify(number_of_offers)


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


def taskKahmsatScraping(res) -> dict:
    myDict = {}
    ORIGN = f"https://khamsat.com"
    URL = ORIGN + "/community/requests"
    try:
        title = res.find('h3', attrs={"class": "details-head"}).find('a').text
        url = ORIGN + \
            res.find('h3', attrs={"class": "details-head"}
                     ).find('a').get_attribute_list('href')[0]
        time = res.find('td', attrs={
                        "class": "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
        url_img = res.find('td', attrs={
                           "class": "avatar-td text-center"}).find('img').get_attribute_list('src')[0]
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
        myDict = {"postId": postId,   "webSiteName": "khamsat", "title": title,
                  "url": url, "time": time, "status": None, "price": None,  "url_img": url_img}
    except Exception as exc:
        print(f"This Exception From khamsat get offer the error is : {exc}")
    return myDict


def taskScrapLinksKhamsat(offer, requests_session):
    myDict = {}
    try:
        webpage2 = requests_session.get(offer["url"], headers=HEADERS)
        soup = BeautifulSoup(webpage2.text, "lxml")
        content = soup.find(name='article', attrs={
                            "class": "replace_urls"}).text
        content = " ".join(content.split())
        number_of_offers = soup.findAll(
            name='div', attrs={"class": "card-header bg-white"})[1].find(name='h3').text
        publisher = soup.find(name='a', attrs={"class": "sidebar_user"}).text
        statusOfPublisher = soup.find(
            name='ul', attrs={"class": "details-list"}).find(name='li').text.strip()
        dateTime = soup.findAll(name='div', attrs={
                                "class": "col-6"})[1].find(name='span').get_attribute_list('title')[0]
        date_time_obj = datetime.strptime(dateTime, '%d/%m/%Y %H:%M:%S GMT')
        dateTime = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        myDict = {"dateTime": dateTime, "publisher": publisher, "statusOfPublisher": statusOfPublisher,
                  "content": content, "number_of_offers": number_of_offers}
        offer.update(myDict)
        return offer
    except Exception as exc:
        print(f"This Exception From mostaql get offer the error is : {exc}")


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
        webpage2 = requests_session.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage2.text, "lxml")
        content = soup.find(name='div', attrs={
                            "class": "text-wrapper-div carda__content"}).text
        content = " ".join(content.split())
        publisher = soup.find(name='h5', attrs={
                              "class": "postcard__title profile__name mrg--an"}).find(name='bdi').text
        status = soup.find(name='bdi', attrs={
                           "class": "label label-prj-open"}).text
        price = soup.find(name='span', attrs={"dir": "rtl"}).text
        url_img = soup.find(name='div', attrs={
                            "class": "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
        dateTime = soup.find(name='td', attrs={
                             "data-type": "project-date"}).find(name='time').get_attribute_list('datetime')[0]
        ########################################################
        myDict = {"postId": postId, "dateTime": dateTime, "publisher": publisher, "statusOfPublisher": None,  "webSiteName": "mostaql", "title": title,
                  "content": content, "url": url, "time": time, "status": status, "price": price, "number_of_offers": number_of_offers, "url_img": url_img}
    except Exception as exc:
        print(f"This Exception From mostaql get offer the error is : {exc}")
    return myDict


def taskScrapKafiil(res, requests_session, budget_min, budget_max) -> dict:
    myDict = {}
    price = res.findAll('p')[0].text.strip()
    list_price = price.split('-')
    numMin = int(list_price[0].strip().removeprefix('$'))
    numMax = int(list_price[1].strip().removeprefix('$'))
    budget_max = int(float(budget_max))
    budget_min = int(float(budget_min))
    if ((budget_min > 0 or budget_max < 10000) and not (numMin >= budget_min and numMax <= budget_max)):
        return
    try:
        title = res.findAll('a')[1].text.split()
        if (title[0] != "قيد"):
            title = " ".join(title[1:])
        else:
            title = " ".join(title[2:])
        url = res.findAll('a')[1].get_attribute_list('href')[0]
        time = res.findAll('span')[1].text.strip()
        status = res.findAll('span')[0].text
        number_of_offers = res.findAll('span')[2].text.strip()
        url_img = res.find('img').get_attribute_list('src')[0]
        postId = url.split('-')[0].split('/')[-1]
        #################################################
        webpage2 = requests_session.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage2.text, "lxml")
        content = soup.find(name='p', attrs={"class": ""}).text
        content = " ".join(content.split())
        publisher = soup.find(
            name='div', attrs={"class": "user-info-row"}).find('div').find('a').text
        publisher = " ".join(publisher.split())
        dateTime = soup.find(name='span', attrs={
                             "data-toggle": "tooltip"}).get_attribute_list('title')[0]
        myDict = {"postId": postId, "dateTime": dateTime, "publisher": publisher, "statusOfPublisher": None,  "webSiteName": "kafiil", "title": title,
                  "content": content, "url": url, "time": time, "status": status, "price": price, "number_of_offers": number_of_offers, "url_img": url_img}
    except Exception as exc:
        print(f"This Exception From kafiil get offer the error is : {exc}")
    return myDict


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
