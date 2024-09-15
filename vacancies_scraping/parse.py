import asyncio
import csv
import time
from dataclasses import dataclass, astuple

import aiohttp
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

BASE_URL = "https://jobs.dou.ua/"
VACANCY_URL = urljoin(BASE_URL, "vacancies/?category=Python")
KEY_WORDS = [
    "Python", "Django", "Flask", "FastAPI", "SQL", "NoSQL", "PostgreSQL", "MySQL",
    "Redis", "Docker", "AWS", "Azure", "API", "Linux", "Artificial Intelligence", "Machine Learning", "OOP",
    "Networking", "Fullstack", "microservices", "algorithms", "asyncio",
    "Git", "REST", "GraphQL", "JavaScript", "JS", "React", "Angular", "HTML", "CSS"
]


@dataclass
class Vacancy:
    title: str
    city: str
    salary: str = None
    technologies: list = None


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


async def fetch_vacancy_detail_soup(session, vacancy_url):
    async with session.get(vacancy_url, params={"switch_lang": "en"}) as response:
        html = await response.text()
        return BeautifulSoup(html, "html.parser")


def get_technology_mentions(text):
    technologies_mentions = set()

    for word in text.split():
        if (
            word in KEY_WORDS
            or word.lower() in KEY_WORDS
            or word.upper() in KEY_WORDS
            or word.capitalize() in KEY_WORDS
        ):
            word = word.capitalize()

            technologies_mentions.add(word)

    return list(technologies_mentions)


def write_to_csv(vacancies):
    with open("../data/technologies.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "City", "Salary", "Technologies"])
        writer.writerows([
            (vacancy.title,
             vacancy.city,
             vacancy.salary,
             ", ".join(vacancy.technologies))
            for vacancy
            in vacancies
        ])


def get_vacancy(soup: BeautifulSoup):
    salary = soup.select_one("span.salary")
    if salary:
        salary = salary.text
        salary = salary[salary.index("$"):]
        print(salary)
    city = soup.select_one("span.place")
    if city:
        city = city.text
    return Vacancy(
        title=soup.select_one("h1.g-h2").text,
        city=city,
        salary=salary,
        technologies=get_technology_mentions(soup.select_one(".b-vacancy").text),
    )


async def count_technology_mentions():
    vacancies = []
    with webdriver.Chrome() as driver:
        driver.get(VACANCY_URL)
        time.sleep(2)
        load_all_vacancies(driver)
        time.sleep(1)
        vacancies_urls = get_all_vacancies(driver)

        async with aiohttp.ClientSession() as session:
            tasks = [
                fetch_vacancy_detail_soup(session, url) for url in vacancies_urls
            ]
            vacancy_soups = await asyncio.gather(*tasks)

            for i, vacancy_detail_soup in enumerate(vacancy_soups):
                vacancies.append(get_vacancy(vacancy_detail_soup))

    write_to_csv(vacancies)


if __name__ == "__main__":
    asyncio.run(count_technology_mentions())
