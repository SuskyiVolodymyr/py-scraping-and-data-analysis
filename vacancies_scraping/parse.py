import asyncio
import time
from urllib.parse import urljoin

import aiohttp
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


def get_all_vacancies(driver):
    vacancies = driver.find_elements(By.CSS_SELECTOR, "li.l-vacancy")
    urls = [
        vacancy.find_element(By.CSS_SELECTOR, "a.vt").get_attribute("href")
        for vacancy in vacancies
    ]
    return urls


async def fetch_vacancy_detail_text(session, vacancy_url):
    async with session.get(vacancy_url) as response:
        html = await response.text()
        return html


async def count_technology_mentions():
    technology_mentions = {}
    with webdriver.Chrome() as driver:
        driver.get(VACANCY_URL)
        time.sleep(2)
        load_all_vacancies(driver)
        time.sleep(1)
        vacancies_urls = get_all_vacancies(driver)

        async with aiohttp.ClientSession() as session:
            tasks = [
                fetch_vacancy_detail_text(session, url) for url in vacancies_urls
            ]
            vacancy_texts = await asyncio.gather(*tasks)


if __name__ == "__main__":
    count_technology_mentions()
