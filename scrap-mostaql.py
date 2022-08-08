from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time as Ti

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
url = 'https://mostaql.com/projects?budget_max=10000&sort=latest'

url = f"https://mostaql.com/projects?page={num_bage}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"

driver.get(url)

listResult = []
results = driver.find_elements(by= By.CLASS_NAME ,value= "project-row")
for res in results:
    title = res.find_element(by= By.XPATH, value= './td/div[1]/div[1]/h2/a').text 
    url = res.find_element(by= By.XPATH, value= './td/div[1]/div[1]/h2/a').get_attribute('href')
    time = res.find_element(by=By.XPATH, value= './td/div[1]/div[1]/ul/li[2]/time ').text                                                                                  
    listResult.append({"title" : title , "url" : url , "time" : time})    


