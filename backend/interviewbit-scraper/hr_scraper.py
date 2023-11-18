from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from flask import *
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
database_name = os.getenv("MONGO_DB_NAME")

app = Flask(__name__)
CORS(app)
app.config[
    "MONGO_URI"
] = f"mongodb+srv://{username}:{password}@cluster0.fyggxfu.mongodb.net/{database_name}?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

categories = ["hr"]
base_url = "https://www.interviewbit.com"


def goto_page(page, category):
    page.goto(f"{base_url}/{category}-interview-questions/")


def scrape_questions(page):
    collection_name = f"{category}-mock-interview-questions"

    soup = BeautifulSoup(page.content(), "lxml")
    sections = soup.find_all("div", {"data-scroll-identifier": "each-article-section"})
    for section in sections:
        heading = section.h2.text.lower()
        if "salary" in heading or "multiple choice" in heading:
            continue
        questions = section.find_all("section", {"class": "ibpage-article-header"})
        for question in questions:
            q = dict()
            q["heading"] = section.h2.text

            h3 = question.h3.text
            if "output" in h3:
                continue
            i = h3.index(".")
            q["question"] = h3[i + 1 :].strip()

            paras = question.find_all("p")

            tips = []
            guidelines = []

            for i in range(len(paras)):
                p = paras[i]

                if "tips to answer" in p.text.lower():
                    tips_list = question.find_all("li")
                    for li in tips_list:
                        tips.append(li.text)
                    if len(tips) == 0:
                        tips.append(paras[i + 1].text)
                        i += 1
                elif "sample answer" in p.text.lower():
                    i += 1
                    answer = ""
                    while i < len(paras):
                        answer += paras[i].text + "\n"
                        i += 1
                    q["answer"] = answer.strip()
                    
                else:
                    if q.get("answer") != None and p.text.lower() in q["answer"].lower():
                        continue
                    guidelines.append(p.text)
                if q.get("answer") == None:
                    blockquote = question.find("blockquote")
                    if blockquote != None:
                        q["answer"] = blockquote.text

            q["answer_tips"] = tips
            q["answer_guidelines"] = guidelines
            db[collection_name].insert_one(q)


p = sync_playwright().start()
chromium = p.chromium
browser = chromium.launch(headless=False, slow_mo=500)
page = browser.new_page()

for category in categories:
    goto_page(page, category)
    scrape_questions(page)
    print("done")
