import requests
from bs4 import BeautifulSoup
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flask import render_template, url_for, flash, redirect, request
from app import app, db, login_manager
from forms import RegistrationForm, LoginForm
from models import User
from flask_login import login_user, current_user, logout_user, login_required
import bcrypt
import requests
import random   
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
from selenium.webdriver.common.action_chains import ActionChains


@app.route("/home", methods=['POST', 'GET'])
@login_required
def home():
     if request.method== "POST":
         keyword= request.form.get('keyword')
         seller_type= request.form.get('seller_type')
         seller_country= request.form.get('seller_country')
         results = scrape_fiverr(keyword, seller_type, seller_country    )
         return render_template('home.html', results= results)
     return render_template('home.html')

def fetch_free_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the table exists
    table = soup.find('table', {'id': 'proxylisttable'})
    if table is None:
        print("Could not find the proxy list table.")
        return []

    proxies = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) > 0:
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxy = f"http://{ip}:{port}"
            proxies.append(proxy)

    return proxies

def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15'
]

def construct_fiverr_url(keyword, seller_type=None, seller_country=None):
    base_url = "https://www.fiverr.com/search/gigs"
    params = {
        'query': keyword,
        'source': 'drop_down_filters'
    }
    if seller_type:
        params['ref'] = f'seller_level%3A{seller_type}'
    if seller_country:
        params['seller_country'] = seller_country
    
    query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
    return f"{base_url}?{query_string}"

def human_like_delay(min_delay=1.5, max_delay=3.5):
    time.sleep(random.uniform(min_delay, max_delay))

def create_driver_with_proxy(proxy):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Replace with your actual path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_fiverr(keyword, seller_type=None, seller_country=None):
    url = construct_fiverr_url(keyword, seller_type, seller_country)
    proxies = load_proxies('D:\\fyp\\Service-Hunting-Tool\\Proxy List.txt')
    results = []

    for proxy in proxies:
        driver = create_driver_with_proxy(proxy)
        try:
            driver.get(url)
            human_like_delay()

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper')))

            listings = driver.find_elements(By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper div.basic-gig-card')
            for gig in listings:
                try:
                    title_element = gig.find_element(By.CSS_SELECTOR, 'a > p')
                    title = title_element.get_attribute('innerText').strip()
                    url = gig.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    price_element = gig.find_element(By.CSS_SELECTOR, 'a span span')
                    price = price_element.text.strip().replace('\u00A0', ' ') if price_element else 'N/A'
                    results.append({'title': title, 'url': url, 'price': price})
                    human_like_delay()  # Add a delay between interactions
                except Exception as e:
                    print(f"Error parsing gig: {e}")
        except Exception as e:
            print(f"Error during scraping with proxy {proxy}: {e}")
        finally:
            driver.quit()

        if results:
            break  # Exit the loop if we have results

    return results

# Example usage

