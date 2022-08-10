from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

finalRes = {}
num_bage = 1
budget_min= 0.00
budget_max = 10000

chrome_options = webdriver.ChromeOptions()

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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , chrome_options=chrome_options)

driver.implicitly_wait(10)
driver.maximize_window()

url = f"https://kafiil.com/kafiil/public/projects?page=1&source=web"

driver.get(url)

listResult = []
results = driver.find_elements(by=By.CLASS_NAME, value='project-box')
print("=================")
print(len(results))
print("=================")

for res in results:    
    title = res.find_element(by= By.XPATH, value= './div[1]/div[1]/div/a').text.split(' ', 1)[1]                                                                                                           
    # url = res.find_element(by= By.XPATH, value= './div[1]/div[1]/div/a').get_attribute('href')
    # time = res.find_element(by=By.XPATH, value= './div[1]/div[1]/div/div/span[1]').text
    # status = res.find_element(by=By.XPATH, value= './div[1]/div[1]/div/a/span').text  
    # price = res.find_element(by=By.XPATH, value= './div[1]/div[2]/p').text 
    # number_of_offers = res.find_element(by=By.XPATH, value= './div[1]/div[1]/div/div/span[2]').text 
    # url_img = res.find_element(by=By.XPATH, value= './td[1]/a/img').get_attribute('src')
    # listResult.append({"title" : title , "url" : url , "time" : time}) 
    print(title)

# print(listResult)   


