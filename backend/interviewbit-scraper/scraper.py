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

categories = ["java", "oops", "dbms", "operating-system"]
base_url = "https://www.interviewbit.com"

def goto_page(page, category):
  page.goto(f"{base_url}/{category}-interview-questions/")

def scrape_questions(page):
  collection_name = f"{category}-mock-interview-questions"

  soup = BeautifulSoup(page.content(), "lxml")
  sections = soup.find_all("div", {"data-scroll-identifier": "each-article-section"})
  for section in sections:
    heading = section.h2.text.lower()
    if "programming" in heading or "conclusion" in heading:
      continue
    questions = section.find_all("section", {"class": "ibpage-article-header"})
    for question in questions:
      q = dict()
      q["heading"] = section.h2.text

      h3 = question.h3.text
      if "output" in h3:
        continue
      i = h3.index(".")
      q["question"] = h3[i + 1 : ].strip()

      paras = question.find_all("p")
      answer = ""
      for p in paras:
        answer += p.text + "\n"
      q["answer"] = answer.strip()

      codes = question.find_all("code")
      q["code"] = []
      for code in codes:
        q["code"].append(code.text)
      
      db[collection_name].insert_one(q)


p = sync_playwright().start()
chromium = p.chromium
browser = chromium.launch(headless=False, slow_mo=500)
page = browser.new_page()

for category in categories:
  goto_page(page, category)
  scrape_questions(page)
  print("done")
