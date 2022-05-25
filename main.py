#!/bin/python3

import os
import time
import random
import argparse

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def init_args():
    parser = argparse.ArgumentParser(
        description="Checker for checking USCIS case status."
    )
    parser.add_argument("--receipt-number", "-r", required=True, help="Receipt number")
    args = parser.parse_args()
    return args

def check_status(receipt_number):
    options = Options()
    options.headless = True
    options.set_preference("devtools.debugger.log", True)
    try:
        browser = webdriver.Firefox(options=options)
    except WebDriverException:
        time.sleep(random.randint(10, 30))
        browser = webdriver.Firefox(options=options)
    browser.set_page_load_timeout(30)
    browser.set_window_size(1920, 1080)
    browser.implicitly_wait(1)
    browser.get("https://egov.uscis.gov/casestatus/landing.do")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.ID, "receipt_number")
        )
    )
    receipt_number_input = browser.find_element(By.ID, "receipt_number")
    receipt_number_input.send_keys(receipt_number)
    check_button = browser.find_element(By.XPATH, "//input[@value='CHECK STATUS']")
    check_button.click()
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'uscis-seal')]")
        )
    )
    status_element = browser.find_element(By.XPATH, "//div[@class='rows text-center']")
    status_title_element = browser.find_element(By.XPATH, "//div[@class='rows text-center']/h1")
    status = status_title_element.text
    print(f"Status: {status}")
    print(f"::set-output name=status::{status}")
    old_status = ""
    if os.path.isfile('status.txt'):
        with open('status.txt', 'r') as f:
            old_status = f.read()
            print(f"Old status: {old_status}")
    with open('status.txt', 'w') as f:
        f.write(status)
    if old_status != status:
        print("Status changed!")
        print(f"::set-output name=status_changed::true")
    else:
        print("Status not changed!")
        print(f"::set-output name=status_changed::false")

def main(args):
    check_status(args.receipt_number)

if __name__ == "__main__":
    return_code = main(init_args())
    exit(return_code)