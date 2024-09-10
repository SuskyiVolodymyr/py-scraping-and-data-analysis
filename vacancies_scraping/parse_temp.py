import asyncio
import csv
import time

import aiohttp
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By

BASE_URL = "https://jobs.dou.ua/"
VACANCY_URL = urljoin(BASE_URL, "vacancies/?category=Python")

KEY_WORDS = [
    "Python", "Django", "Flask", "FastAPI", "SQL", "NoSQL", "PostgreSQL", "MySQL",
    "Redis", "Docker", "AWS", "Azure", "API", "Linux", "Artificial Intelligence", "Machine Learning", "OOP",
    "Networking", "Fullstack", "microservices", "algorithms", "asyncio",
    "Git", "REST", "GraphQL", "JavaScript", "JS", "React", "Angular", "HTML", "CSS"
]


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


def get_technology_mentions(text):
    technologies_mentions = {}

    for word in text.split():
        if (
            word in KEY_WORDS
            or word.lower() in KEY_WORDS
            or word.upper() in KEY_WORDS
            or word.capitalize() in KEY_WORDS
        ):
            word = word.capitalize()

            if word in technologies_mentions:
                technologies_mentions[word] += 1
            else:
                technologies_mentions[word] = 1

    return technologies_mentions


def add_technology_mentions(technologies_mentions, new_technology_mentions):
    for key, value in new_technology_mentions.items():
        if key in technologies_mentions:
            technologies_mentions[key] += value
        else:
            technologies_mentions[key] = value

    return technologies_mentions


def write_to_csv(technologies_mentions):
    with open("technologies.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Technology", "Count"])
        writer.writerows([[key, value] for key, value in technologies_mentions.items()])


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

            for vacancy_detail_text in vacancy_texts:
                new_technology_mentions = get_technology_mentions(vacancy_detail_text)
                technology_mentions = add_technology_mentions(
                    technology_mentions,
                    new_technology_mentions
                )

    write_to_csv(technology_mentions)


if __name__ == "__main__":
    asyncio.run(count_technology_mentions())
