import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, time
from twilio.rest import Client



def is_time_between(begin_time, end_time):
    check_time = datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: 
        return check_time >= begin_time or check_time <= end_time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

results = {}

PAGETIMEOUT = 12

try:
    driver.get("https://www.amazon.co.uk/dp/B08H95Y452")
    element = WebDriverWait(driver, PAGETIMEOUT).until(
        EC.presence_of_element_located((By.ID, "outOfStock"))
    )
    instock_amazon = False
except TimeoutException:
    instock_amazon = True
finally:
    results["Amazon"] = instock_amazon


try:
    driver.get("https://www.game.co.uk/playstation-5")
    element = WebDriverWait(driver, PAGETIMEOUT).until(
        EC.presence_of_element_located((By.ID, "contentPanels3"))
    )
    game_text = element.\
        find_element_by_class_name("sectionButton").\
        find_element_by_tag_name("a").\
        text.\
        upper()
    instock_game = False if game_text == "OUT OF STOCK" else True
except TimeoutException:
    instock_game = True
finally:
    results["GAME"] = instock_game


try:
    driver.get("https://www.argos.co.uk/product/8349000")
    element = WebDriverWait(driver, PAGETIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "add-to-trolley-main"))
    )
    argos_text = element.\
        find_element_by_tag_name("button").\
        text.\
        replace("\n", " ").\
        upper()
    instock_argos = True if argos_text == "ADD TO TROLLEY" else False
except TimeoutException:
    instock_argos = False
finally:
    results["Argos"] = instock_argos


try:
    driver.get("https://www.johnlewis.com/browse/electricals/gaming/playstation/console/_/N-2pehZ1z0pdgi")
    element = WebDriverWait(driver, PAGETIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//section[@data-product-id='5115192']"))
    )
    jl_text = element.text.upper()
    instock_jl = False if "OUT OF STOCK" in jl_text else True 
except TimeoutException:
    instock_jl = False
finally:
    results["John Lewis"] = instock_jl


try:
    driver.get("https://www.currys.co.uk/gbuk/sony-ps5/console-gaming/consoles/634_4783_32541_49_ba00013671-bv00313579/xx-criteria.html")
    element = WebDriverWait(driver, PAGETIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "resultList"))
    )
    instock_currys = False if "NO RESULTS WERE FOUND FOR YOUR SEARCH" in element.text.upper() else True
except TimeoutException:
    instock_currys = False
finally:
    results["Currys"] = instock_currys


driver.close()


print(results)

RESULTS_STRING = "\n".join([ "{} = {}".format(i,j) for i,j in results.items()])
MESSAGE_STRING = "Found a PlayStation !\n" + RESULTS_STRING

FOUND_PLAYSTATION = any([j for i,j in results.items()])
CAN_SEND_MESSAGE = not is_time_between(time(11,00), time(7,30))

#if FOUND_PLAYSTATION and CAN_SEND_MESSAGE:
if True:
    client = Client(
        os.environ['TWILIO_ACCOUNT_SID'], 
        os.environ['TWILIO_AUTH_TOKEN']
    )
    
    message = client.messages.create(
        body=MESSAGE_STRING,
        from_=os.environ['TWILIO_FROM_NUMBER'],
        to=os.environ['TWILIO_TO_NUMBER']
    )

