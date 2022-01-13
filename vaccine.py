import time
import logging
import argparse
from slack import WebClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level = logging.INFO, format = "%(asctime)s %(levelname)s %(message)s")

url = "https://www.nhs.uk/conditions/coronavirus-covid-19/coronavirus-vaccination/book-coronavirus-vaccination/"

def main():

    args = parse_args()
    if args.visible:
        driver = webdriver.Chrome()
    else:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    driver.get(url)

    elem = driver.find_element_by_link_text("Book my appointments")
    elem.click()

    while True:
        elems = driver.find_elements_by_xpath("//h1")
        if len(elems) == 1 and elems[0].text == "You are in a queue":
            logging.info("In a queue")
            time.sleep(60)
        else:
            break

    # NHS number
    elem = driver.find_element_by_id("option_No_input")
    elem.click()

    elem = driver.find_element_by_id("submit-button")
    elem.click()

    # Name
    elem = driver.find_element_by_id("Firstname")
    elem.click()
    elem.send_keys("Ben")
    elem = driver.find_element_by_id("Surname")
    elem.send_keys("Smith")
    elem = driver.find_element_by_id("submit-button")
    elem.click()

    # DOB
    elem = driver.find_element_by_id("Date_Day")  
    elem.click()
    elem.send_keys("01")
    elem = driver.find_element_by_id("Date_Month")
    elem.send_keys("01")
    elem = driver.find_element_by_id("Date_Year")
    elem.send_keys("1990")
    elem = driver.find_element_by_id("submit-button")
    elem.click()

    # Postcode
    elem = driver.find_element_by_id("Postcode")
    elem.send_keys("SW1A 0AA")
    elem = driver.find_element_by_id("submit-button")
    elem.click()

    # Flu
    elem = driver.find_element_by_id("option_No_input")
    elem.click()

    elem = driver.find_element_by_id("submit-button")
    elem.click()

    # Flu
    elem = driver.find_element_by_id("option_No_input")
    elem.click()

    elem = driver.find_element_by_id("submit-button")
    elem.click()

    # Essential or social care worker
    elem = driver.find_element_by_id("option_Neither_input")
    elem.click()
    elem = driver.find_element_by_id("submit-button")
    elem.click()

    elem = driver.find_element_by_id("page_h1_title")

    slack_client = WebClient('000000000')

    if elem.text == 'You are not currently eligible to book through this service':
        slack_client.chat_postMessage(channel="000000", text="Not eligible")
        logging.info("Not eligible")
    else:
        slack_client.chat_postMessage(channel="000000", text="Maybe eligible? https://www.nhs.uk/book-a-coronavirus-vaccination/do-you-have-an-nhs-number")
        logging.warning("Maybe eligible? Website says: %s", elem.text)

    driver.quit()

def parse_args():
    parser = argparse.ArgumentParser(description="Check if I'm eligible")
    parser.add_argument("--visible", action="store_true", help="run with a visible browser")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
