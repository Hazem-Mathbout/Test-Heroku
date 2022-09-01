import json
from bs4 import BeautifulSoup
import requests
import concurrent.futures

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
def scrapKhamsat(output = None):
    ORIGN = f"https://khamsat.com"
    URL = ORIGN +"/community/requests"
    try:
        output = request.get_json()
    except Exception as exc:
        print(f'generated an exception: {exc}')
    
    finalRes = {}
    listResult = []
    basePage = requests.get(URL, headers=HEADERS)
    baseSoup = BeautifulSoup(basePage.content, "html.parser")

    results = baseSoup.findAll(name='tr', attrs={"class" : "forum_post"})
    for i, res in enumerate(results):
        title = res.find('h3', attrs={"class" : "details-head"}).find('a').text
        url = ORIGN + res.find('h3', attrs={"class" : "details-head"}).find('a').get_attribute_list('href')[0]
        time = res.find('td', attrs={"class" : "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
        url_img = res.find('td', attrs={"class" : "avatar-td text-center"}).find('img').get_attribute_list('src')[0]
        postId = res.get('id').replace("forum_post-", "posts_ids%5B%5D=")


        # ####################################

        webpage2 = requests.get(url, headers= HEADERS)
        soup = BeautifulSoup(webpage2.content, "html.parser")
        content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
        content = " ".join(content.split())
        number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
        publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
        statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
        dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]

        #####################################
                                 
        listResult.append({"postId" :postId , "dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher ,  "webSiteName" : "khamsat" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : number_of_offers , "url_img" : url_img})
    # for res in listResult:
    #     finalRes.update(res)
    finalRes = json.dumps(listResult)
    return (finalRes)

 
@app.route("/resMost", methods = ["POST" , "GET"])
def scrapmostaql(output = None):
    try:
         output = request.get_json()
    except Exception as exc:
        print(exc)   
    budget_max = 10000 if output["budget_max"]=="None" else output["budget_max"]
    budget_min = 0.00  if output["budget_min"]=="None" else output["budget_min"]
    num_bage_mostaql   = 1     if output["num_bage_mostaql"]=="None" or 0 else output["num_bage_mostaql"]
    category_mostaql = output["category_mostaql"]

    finalRes = {}
    listResult = []
    
    if category_mostaql == "None" : 
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    else:
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&category={category_mostaql}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    sourcPage = requests.get(URL, headers=HEADERS)
    sourcSoup = BeautifulSoup(sourcPage.content, "html.parser")
    tempRes = sourcSoup.findAll(name='tr', attrs={"class" : "project-row"})
    if(len(tempRes) != 0):
        for res in tempRes:
            title = res.find('a').text
            url = res.find('a').get_attribute_list('href')[0]
            time = res.find('time').text.strip()
            time = "".join(time.split())  
            number_of_offers = res.find('ul').findAll('li')[2].text.strip()
            postId = url.split('-')[0].split('/')[-1]
            ########################################################
            webpage2 = requests.get(url, headers= HEADERS)
            soup = BeautifulSoup(webpage2.content, "html.parser")
            content = soup.find(name= 'div' , attrs={"class" : "text-wrapper-div carda__content"}).text
            content = " ".join(content.split())
            publisher = soup.find(name='h5' , attrs={"class" : "postcard__title profile__name mrg--an"}).find(name='bdi').text
            status = soup.find(name='bdi', attrs={"class" : "label label-prj-open"}).text
            price = soup.find(name='span', attrs={"dir" : "rtl"}).text
            url_img = soup.find(name='div' , attrs={"class" : "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
            dateTime = soup.find(name= 'td', attrs={"data-type" : "project-date"}).find(name='time').get_attribute_list('datetime')[0]
            ########################################################          
                                                                                                                                                           
            listResult.append({"postId" : postId , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "mostaql" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
          
    
    finalRes = json.dumps(listResult)
    return (finalRes)
    


@app.route("/resKafi", methods = ["POST" , "GET"])
def scrapkafiil(output = None):
    try:
        output = json.loads(request.data, strict = False)
    except Exception as exc:
        print(exc)  
    num_bage_kafiil   = 1 if output["num_bage_kafiil"]=="None" or 0 else output["num_bage_kafiil"]
    category_kafiil = output["category_kafiil"]

    finalRes = {}
    listResult = []
    
    if category_kafiil == "None" : 
        URL = f"https://kafiil.com/kafiil/public/projects?page={num_bage_kafiil}&source=web"
    else:
        URL = f"https://kafiil.com/kafiil/public/projects/{category_kafiil}?page={num_bage_kafiil}&search=&source=web"
    sourcPage = requests.get(URL, headers=HEADERS)    
    sourcSoup = BeautifulSoup(sourcPage.content, "html.parser")
    tempRes = sourcSoup.findAll(name='div', attrs={"class" : "project-box active"})
    if len(tempRes) != 0 :
            for res in tempRes: 
                title = res.findAll('a')[1].text.split()
                if(title[0] != "قيد"):
                    title = " ".join(title[1:])
                else:
                    title=" ".join(title[2:])
                url = res.findAll('a')[1].get_attribute_list('href')[0]
                time = res.findAll('span')[1].text.strip()
                status = res.findAll('span')[0].text
                price = res.findAll('p')[0].text.strip()
                number_of_offers = res.findAll('span')[2].text.strip()
                url_img = res.find('img').get_attribute_list('src')[0]
                postId = url.split('-')[0].split('/')[-1]
                #################################################
                webpage2 = requests.get(url, headers= HEADERS)
                soup = BeautifulSoup(webpage2.content, "html.parser")
                content = soup.find(name= 'p' , attrs={"class" : ""}).text
                content = " ".join(content.split())
                publisher = soup.find(name='div' , attrs={"class" : "user-info-row"}).find('div').find('a').text
                publisher = " ".join(publisher.split())
                dateTime = soup.find(name= 'span', attrs={"data-toggle" : "tooltip"}).get_attribute_list('title')[0]
                #################################################
                listResult.append({"postId" : postId  , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "kafiil" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
         
    
    finalRes = json.dumps(listResult)
    return (finalRes)


@app.route("/resLoadMoreKhamsat", methods = ["POST", "GET"])
def scrapKhamsatLoadMore():
    output = json.loads(request.data, strict = False)
    URL = "https://khamsat.com/ajax/load_more/community/requests"
    ORIGN = f"https://khamsat.com"
    dataLoadMore   = output["dataLoadMore"]
    finalRes = {}
    listResult = []
    response = requests.post(URL, headers=HEADERS, data=dataLoadMore)
      
    body = response.json()
    htmlString = body["content"]
    sourcSoup = BeautifulSoup(htmlString, "html.parser")
   
    results = sourcSoup.findAll(name='tr', attrs={"class" : "forum_post"})
    for i, res in enumerate(results):
        title = res.find('h3', attrs={"class" : "details-head"}).find('a').text
        url = ORIGN + res.find('h3', attrs={"class" : "details-head"}).find('a').get_attribute_list('href')[0]
        time = res.find('td', attrs={"class" : "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
        url_img = res.find('td', attrs={"class" : "avatar-td text-center"}).find('img').get_attribute_list('src')[0]
        postId = res.get('id').replace("forum_post-", "posts_ids%5B%5D=")


        # ####################################

        webpage2 = requests.get(url, headers= HEADERS)
        soup = BeautifulSoup(webpage2.content, "html.parser")
        content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
        content = " ".join(content.split())
        number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
        publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
        statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
        dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]

        #####################################
                                 
        listResult.append({"postId" :postId , "dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher ,  "webSiteName" : "khamsat" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : number_of_offers , "url_img" : url_img})
    # for res in listResult:
    #     finalRes.update(res)
   
    finalRes = json.dumps(listResult)
    return (finalRes)

@app.route('/home', methods = ["POST", "GET"])
def offersForHome():
    allData = []
    payload = json.loads(request.data, strict = False)
    postedData   = payload["route"]
    if "/resLoadMoreKhamsat" in postedData:
        LISTSCRAPING = [scrapkafiil, scrapKhamsatLoadMore, scrapmostaql]
    else:
        LISTSCRAPING = [scrapKhamsat, scrapkafiil,scrapmostaql]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_website = {executor.submit(website, payload): website for website in LISTSCRAPING}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (website, exc))
            else:
                output = json.loads(data)
                allData.extend(output)
    finalRes = json.dumps(allData)
    return (finalRes)


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)