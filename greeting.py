from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time as Ti
import os
from bs4 import BeautifulSoup
import requests

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

# def mainScrape():
#     output = request.get_json()
#     num = output["num"]
#     listResult = scrapKhamsat(num=num)
#     return (listResult)   

@app.route("/resKham", methods = ["POST" , "GET"])
def scrapKhamsat():
    output = request.get_json()
    num = output["num"]
    finalRes = {}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

 
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    driver.implicitly_wait(10)
    driver.maximize_window()
    url = 'https://khamsat.com/community/requests'
    driver.get(url)

    for i in range(num):
      try:  
        elemnt = driver.switch_to.active_element
        btn = elemnt.find_element(by=By.XPATH, value='//*[@id="community_loadmore_btn"]')
        driver.execute_script("arguments[0].click();", btn)
        Ti.sleep(2)
      except Exception as e:
        print (e)
        break
    listResult = []
    results = driver.find_elements(by= By.CLASS_NAME ,value= "forum_post")
    for res in results:
        title = res.find_element(by= By.XPATH, value= './td[2]/h3').text
        url = res.find_element(by= By.XPATH, value= './td[2]/h3/a').get_attribute('href')
        time = res.find_element(by=By.XPATH, value= './td[2]/ul/li[2]/span').text
        url_img = res.find_element(by=By.XPATH, value= './td[1]/a/img').get_attribute('src')


        # ####################################

        webpage = requests.get(url, headers= HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        content = soup.find(name= 'article' , attrs={"class" : "replace_urls"}).text
        content = " ".join(content.split())
        number_of_offers = soup.findAll(name='div' , attrs={"class" : "card-header bg-white"})[1].find(name='h3').text
        publisher = soup.find(name='a' , attrs={"class" : "sidebar_user"}).text
        statusOfPublisher = soup.find(name='ul', attrs={"class" : "details-list"}).find(name='li').text.strip()
        dateTime = soup.findAll(name= 'div', attrs={"class" : "col-6"})[1].find(name='span').get_attribute_list('title')[0]
        # copyDriver.get(url)
        # publisher = ""
        # statusOfPublisher = ""
        # number_of_offers = copyDriver.find_element(by=By.XPATH, value= '/html/body/div[2]/div/div[2]/div/div[3]/div[2]/div[3]/div[1]/h3').text
        # content = copyDriver.find_element(by=By.CLASS_NAME, value='replace_urls').text
        # results_1 = copyDriver.find_elements(by= By.CLASS_NAME ,value= "details-td.avatar-td__small-padding")
        # for res in results_1:
        #     publisher = res.find_element(by= By.XPATH, value= './h3').text
        #     statusOfPublisher = res.find_element(by=By.XPATH, value= './ul').text
        # ####################################

                                 
        listResult.append({"dateTime" : dateTime ,"publisher" : publisher , "statusOfPublisher" : statusOfPublisher ,  "webSiteName" : "khamsat" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : None , "price" : None , "number_of_offers" : number_of_offers , "url_img" : url_img})
    # for res in listResult:
    #     finalRes.update(res)
    finalRes = json.dumps(listResult)
    return (finalRes)

 
@app.route("/resMost", methods = ["POST" , "GET"])
def scrapmostaql():
    output = request.get_json()
    budget_max = 10000 if output["budget_max"]=="None" else output["budget_max"]
    budget_min = 0.00  if output["budget_min"]=="None" else output["budget_min"]
    num_bage   = 1     if output["num_bage"]=="None" else output["num_bage"]
    category = output["category"]

    finalRes = {}
    listResult = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    for page in range(num_bage):
        if category == "None" : 
            url = f"https://mostaql.com/projects?page={page+1}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
        else:
            url = f"https://mostaql.com/projects?page={page+1}&category={category}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
        driver.get(url)
        tempRes = driver.find_elements(by= By.CLASS_NAME ,value= "project-row")
        if(len(tempRes) != 0):
            for res in tempRes:
                title = res.find_element(by= By.XPATH, value= './td/div[1]/div[1]/h2/a').text 
                url = res.find_element(by= By.XPATH, value= './td/div[1]/div[1]/h2/a').get_attribute('href')
                time = res.find_element(by=By.XPATH, value= './td/div[1]/div[1]/ul/li[2]/time ').text   
                number_of_offers = res.find_element(by=By.XPATH, value= './td/div[1]/div[1]/ul/li[3]').text
                ########################################################
                webpage = requests.get(url, headers= HEADERS)
                soup = BeautifulSoup(webpage.content, "html.parser")
                content = soup.find(name= 'div' , attrs={"class" : "text-wrapper-div carda__content"}).text
                content = " ".join(content.split())
                publisher = soup.find(name='h5' , attrs={"class" : "postcard__title profile__name mrg--an"}).find(name='bdi').text
                status = soup.find(name='bdi', attrs={"class" : "label label-prj-open"}).text
                price = soup.find(name='span', attrs={"dir" : "rtl"}).text
                url_img = soup.find(name='div' , attrs={"class" : "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
                dateTime = soup.find(name= 'td', attrs={"data-type" : "project-date"}).find(name='time').get_attribute_list('datetime')[0]
                ########################################################          
                                                                                                                                                               
                listResult.append({"dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "mostaql" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
        else:
            break    
    
    finalRes = json.dumps(listResult)
    return (finalRes)
    


@app.route("/resKafi", methods = ["POST" , "GET"])
def scrapkafiil():
    output = request.get_json()
    num_bage   = 1 if output["num_bage"]=="None" else output["num_bage"]
    category = output["category"]
    # open_offer = output["open"]

    finalRes = {}
    listResult = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    for page in range(num_bage):
        if category == "None" : 
            url = f"https://kafiil.com/kafiil/public/projects?page={page+1}&source=web"
        else:
            url = f"https://kafiil.com/kafiil/public/projects/{category}?page={page+1}&search=&source=web"
            
        driver.get(url)
        tempRes = driver.find_elements(by=By.CLASS_NAME, value='project-box')
        if len(tempRes) != 0 :
            for res in tempRes: 
                title = res.find_element(by= By.XPATH, value= './div[1]/div[1]/div/a').text.split()
                if(title[0] != "قيد"):
                    title = " ".join(title[1:])
                else:
                    title=" ".join(title[2:])
                url = res.find_element(by= By.XPATH, value= './div[1]/div[1]/div/a').get_attribute('href')
                time = res.find_element(by=By.XPATH, value= './div[1]/div[1]/div/div/span[1]').text 
                status = res.find_element(by=By.XPATH, value= './div[1]/div[1]/div/a/span').text
                price = res.find_element(by=By.XPATH, value= './div[1]/div[2]/p').text
                number_of_offers = res.find_element(by=By.XPATH, value= './div[1]/div[1]/div/div/span[2]').text
                url_img = res.find_element(by=By.XPATH, value= './div[1]/div[1]/a/img').get_attribute('src')

                #################################################
                webpage = requests.get(url, headers= HEADERS)
                soup = BeautifulSoup(webpage.content, "html.parser")
                content = soup.find(name= 'p' , attrs={"class" : ""}).text
                content = " ".join(content.split())
                publisher = soup.find(name='div' , attrs={"class" : "user-info-row"}).find('div').find('a').text
                publisher = " ".join(publisher.split())
                dateTime = soup.find(name= 'span', attrs={"data-toggle" : "tooltip"}).get_attribute_list('title')[0]
                #################################################
                listResult.append({"dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "kafiil" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
        else:
            break    
    
    finalRes = json.dumps(listResult)
    return (finalRes)




@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)