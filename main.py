#!/bin/python3

import os
import argparse

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(1)
    driver.get("https://egov.uscis.gov/casestatus/landing.do")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "receipt_number")
        )
    )
    receipt_number_input = driver.find_element(By.ID, "receipt_number")
    receipt_number_input.send_keys(receipt_number)
    check_button = driver.find_element(By.XPATH, "//input[@value='CHECK STATUS']")
    check_button.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'uscis-seal')]")
        )
    )
    status_element = driver.find_element(By.XPATH, "//div[@class='rows text-center']")
    status_title_element = driver.find_element(By.XPATH, "//div[@class='rows text-center']/h1")
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