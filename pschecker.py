import os
import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from twilio.rest import Client

PAGETIMEOUT = 15


def save_as_file(driver, name):
    with open(name, "w") as fi:
        html = driver.page_source
        fi.write(html)


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % get_proxy())
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=chrome_options)


def send_message(msg):
    client = Client(
        os.environ['TWILIO_ACCOUNT_SID'],
        os.environ['TWILIO_AUTH_TOKEN']
    )
    client.messages.create(
        body=msg,
        from_=os.environ['TWILIO_FROM_NUMBER'],
        to=os.environ['TWILIO_TO_NUMBER']
    )


def check_amazon(driver):
    try:
        driver.get("https://www.amazon.co.uk/dp/B08H95Y452")
        WebDriverWait(driver, PAGETIMEOUT).until(
            EC.presence_of_element_located((By.ID, "outOfStock"))
        )
        return False
    except TimeoutException:
        driver.get_screenshot_as_file("screenshot.png")
        return True
    finally:
        save_as_file(driver, "log/amazon.html")



def check_game(driver):
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
        return False if game_text == "OUT OF STOCK" else True
    except TimeoutException:
        return True
    finally:
        save_as_file(driver, "log/game.html")


def check_argos(driver):
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
        return True if argos_text == "ADD TO TROLLEY" else False
    except TimeoutException:
        return False
    finally:
        save_as_file(driver, "log/argos.html")


def check_johnlewis(driver):
    try:
        driver.get("https://www.johnlewis.com/browse/electricals/gaming/playstation/console/_/N-2pehZ1z0pdgi")
        element = WebDriverWait(driver, PAGETIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//section[@data-product-id='5115192']"))
        )
        jl_text = element.text.upper()
        return False if "OUT OF STOCK" in jl_text else True
    except TimeoutException:
        return False
    finally:
        save_as_file(driver, "log/johnlewis.html")


def check_currys(driver):
    try:
        driver.get("https://www.currys.co.uk/gbuk/sony-ps5/console-gaming/consoles/634_4783_32541_49_ba00013671-bv00313579/xx-criteria.html")
        element = WebDriverWait(driver, PAGETIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "resultList"))
        )
        return False if "NO RESULTS WERE FOUND FOR YOUR SEARCH" in element.text.upper() else True
    except TimeoutException:
        return False
    finally:
        save_as_file(driver, "log/currys.html")


def get_proxy():
    # res = requests.get("http://pubproxy.com/api/proxy?format=txt")
    # return res.text
    return ""


if __name__ == "__main__":
    driver = get_chrome_driver()
    results = {
        "Amazon": check_amazon(driver),
        "Game": check_game(driver) and check_game(driver),
        "Currys": check_currys(driver),
        "Argos": check_argos(driver),
        "John Lewis": check_johnlewis(driver)
    }
    driver.close()
    pprint.pprint(results)
    FOUND_PLAYSTATION = any([j for i, j in results.items()])
    if FOUND_PLAYSTATION:
        RESULTS_STRING = "\n".join(["{} = {}".format(i, j) for i, j in results.items()])
        MESSAGE_STRING = "Found a PlayStation !\n" + RESULTS_STRING
        send_message(MESSAGE_STRING)
