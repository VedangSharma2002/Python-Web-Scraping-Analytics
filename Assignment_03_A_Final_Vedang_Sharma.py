import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# I decided to scrape job posting for project co-ordinator roles from a website called Workpolis.
# Project co-ordinator jobs are personal to me and reflect on the kind of jobs hope to work at upon finishing school.
# Set up the path to my local ChromeDriver
# This was annoying to set up but works now

DRIVER_PATH = r"C:\Users\Vedang Sharma\Desktop\BBA SCHOOL NOTES\PYTHON FOR DATA ANALYSIS\chromedriver-win64\chromedriver.exe"
browser = webdriver.Chrome(service=Service(DRIVER_PATH))

# I store all scraped data into an empty list or array
job_data = []


# Loop through the first 3 pages of job search results. Sample code provided in labs was heavily referenced.
for page in range(1, 4):  # Pages 1 to 3
    URL = f"https://www.workopolis.com/search?q=project+coordinator&l=burnaby%2C+bc&page={page}"
    browser.get(URL)
    time.sleep(3)
    # Grabbing the content
    content = browser.find_elements(By.CSS_SELECTOR, "li.css-0")
    # Parsing each listing
    for e in content:
        start = e.get_attribute('innerHTML')
        soup = BeautifulSoup(start, "lxml")
        text = soup.get_text().strip()
        lines = text.split("\n")
        lines = [line.strip() for line in lines if line.strip() != ""]

        if len(lines) >= 1:
            main_line = lines[0]

            if "—" in main_line:
                parts = main_line.split("—")
                title_company = parts[0].strip()
                location_raw = parts[1].strip().replace("\xa0", "")
                location = " ".join(location_raw.split()[:2])

                for i in range(len(title_company) - 1, 0, -1):
                    if title_company[i].isupper() and title_company[i - 1] == " ":
                        title = title_company[:i].strip()
                        company = title_company[i:].strip()
                        break
                else:
                    title = title_company
                    company = "N/A"

                job_data.append([title, company, location])
# Converting the scraped data into a dataframe using Pandas library like shown in labs
df = pd.DataFrame(job_data, columns=["Title", "Company", "Location"])
print(df.head(2))
print(df.tail(2))
# finally saving to a csv file
df.to_csv("project_jobs.csv", index=False)
df2 = pd.read_csv("project_jobs.csv")
print(df2.head(2))
print(df2.tail(2))
