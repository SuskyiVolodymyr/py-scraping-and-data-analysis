import time
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By


BASE_URL = "https://jobs.dou.ua/"
VACANCY_URL = urljoin(BASE_URL, "vacancies/?category=Python")


def load_all_vacancies(driver):
    while True:
        try:
            button = driver.find_element(By.CSS_SELECTOR, ".more-btn a")
            button.click()
        except ElementNotInteractableException:
            print("all vacancies loaded")
            break
        time.sleep(1)


def count_technology_mentions():
    with webdriver.Chrome() as driver:
        driver.get(VACANCY_URL)
        time.sleep(2)
        load_all_vacancies(driver)


if __name__ == "__main__":
    count_technology_mentions()