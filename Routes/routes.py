from flask import render_template, url_for, flash, redirect, request
from app import app, login_manager
from Forms.forms import RegistrationForm, LoginForm
from Model.db_models import User
from flask_login import login_user, current_user, logout_user, login_required
import bcrypt
import requests
import random   
# from database_conf.db_config import redis_connect
import json
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
from Model.db_models import db, SearchKeyword,Listing
from datetime import datetime, timedelta
import csv
from Analysis.Data_Analysis import analyze_data,plot_sales_distribution,plot_focus_keywords,plot_unique_keywords_count,generate_wordcloud


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        # Note: bcrypt.hashpw() returns bytes, so decode it before storing in DB
        hashed_password_str = hashed_password.decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password_str)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route("/home", methods=['POST', 'GET'])
# @login_required
# def home():
#     if request.method == "POST":
#         keyword = request.form.get('keyword')
#         seller_type = request.form.get('seller_type')
#         seller_country = request.form.get('seller_country')
#         results = scrape_fiverr(keyword, seller_type, seller_country)
#         return render_template('home.html', results=results)
#     return render_template('home.html')

chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"


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
from playwright.sync_api import sync_playwright
import random
import time
def construct_fiverr_url(keyword, seller_type=None, seller_location=None):
     base_url = "https://www.fiverr.com/search/gigs"
     #base_url= "https://www.fiverr.com"
     params = {
         'query': keyword,
         'source': 'drop_down_filters'
     }
     if seller_type:
         params['ref'] = f'seller_level%3A{seller_type}'
     if seller_location:
         params['ref'] = f'seller_location%3A{seller_location}'
     query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
     print(f"{base_url}?{query_string}")
     return f"{base_url}?{query_string}"
     #return base_url


def human_like_delay(min_delay=1.5, max_delay=3.5):
     time.sleep(random.uniform(min_delay, max_delay))


def simulate_human_interaction(page):
    page.mouse.move(random.randint(0, 1000), random.randint(0, 800))
    human_like_delay()
    page.mouse.click(random.randint(0, 1000), random.randint(0, 800))
    human_like_delay()
    page.keyboard.press('ArrowDown')
    human_like_delay()
    page.keyboard.press('ArrowUp')
    human_like_delay()


def scrape_fiverr(keyword, seller_type=None, seller_country=None,search_id= None):
     url = construct_fiverr_url(keyword, seller_type, seller_country)
     results = []

     with sync_playwright() as p:
         browser = p.chromium.launch(headless=False)
         #browser= p.firefox.launch(headless=False)
         context = browser.new_context(user_agent=random.choice(user_agents))
         page = context.new_page()

         page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/',
            'DNT': '1'
        })

         try:
             human_like_delay()
             page.goto(url)
             human_like_delay()

             #simulate_human_interaction(page)

             listings = page.query_selector_all('div.gig-wrapper-impressions.gig-wrapper div.basic-gig-card')
             for gig in listings:
                 try:
                     title_element = gig.query_selector('a > p')
                     title = title_element.inner_text().strip()
                    #  print('title:', title)
                     url = gig.query_selector('a').get_attribute('href')
                     price_element = gig.query_selector('a span span')
                     price = price_element.inner_text().strip().replace('\u00A0', ' ') if price_element else 'N/A'
                    #  print('price:',price)
                     rating_element = gig.query_selector('div.orca-rating strong.rating-score')
                     rating_score = rating_element.inner_text().strip() if rating_element else 'N/A'
                    #  print('Rating', rating_score)
                     rating_count_element = gig.query_selector('div.orca-rating  span.rating-count-number')
                     rating_count = rating_count_element.inner_text().strip() if rating_count_element else 'N/A'
                    #  print('Raitng Count', rating_count)
                    #  last_delivery = datetime.utcnow() - timedelta(days=random.randint(1, 30))
                    #  print('last delivery', last_delivery)
                     seller= request.form.get('seller_type')
                     lissting= Listing(
                         search_id= search_id,
                         title= keyword,
                         description=title,
                         sales= rating_count,
                         rating= rating_score,
                         industry= 'Technology',
                         platform= 'Fiverr',
                        #  last_delivery= last_delivery,
                         seller_rank= seller
                     )
                     
                     

                     

                     


                     
                     db.session.add(lissting)
                     db.session.commit()
                     results.append({'title': title, 'url': url, 'price': price, 'Rating': rating_score, 'RatingCount':rating_count})
                     human_like_delay()  # Add a delay between interactions
                 except Exception as e:
                     print(f"Error parsing gig: {e}")
         except Exception as e:
             print(f"Error during scraping: {e}")
         finally:
             browser.close()
     return results






@app.route("/home", methods=['POST', 'GET'])
@login_required
def home():
      if request.method == "POST":
          keyword = request.form.get('keyword')
          seller_type = request.form.get('seller_type')
          seller_location = request.form.get('seller_country')
          print(f'Curent user:', current_user.id)
        
          search_keyword=SearchKeyword(
             user_id= current_user.id,
             keywords= keyword,
             seller_type= seller_type,
             seller_country= seller_location
          )
        #   db.session.add(search_keyword)
        #   db.session.commit()
          search_id= search_keyword.keywords
          print("this is a Searchid ++++++++++++++", search_id)
          scrapped_data=scrape_fiverr(keyword, seller_type, seller_location,search_id)
          print('this is scrapped data', scrapped_data)

        #   redis_connect.redis_client.set('scraped_data', json.dumps(scrapped_data))

          

          analysis_results = analyze_data(scrapped_data)

          print('This is analyzed data', analysis_results)


        #   sales_chart = plot_sales_distribution(analysis_results['sales_distribution'])
        #   rating_chart = plot_rating_distribution(analysis_results['rating_distribution'])
          focus_keywords_chart = plot_focus_keywords(analysis_results['focus_keywords'])

          
          sales_distribution_chart = plot_sales_distribution(
                analysis_results['low_sales_count'],
                analysis_results['high_sales_count'])
        #   unique_keywords_chart = plot_unique_keywords_count(analysis_results['unique_keywords'])
          unique_keywords_cloud = generate_wordcloud(analysis_results['unique_keywords'])
          context = {
        'focus_keywords_chart': focus_keywords_chart,
        'sales_distribution_chart': sales_distribution_chart,
        'unique_keywords_cloud': unique_keywords_cloud,
        }
        # avg_rating_chart = plot_average_rating(analysis_results['avg_rating'])
          #results = Listing.query.filter_by(search_id=search_id).all()
        #   results = Listing.query.join(SearchKeyword).filter(SearchKeyword.keywords == search_id).all()

        #avg_rating_chart=avg_rating_chart
        

    #   return render_template('home.html', sales_chart=sales_chart, rating_chart=rating_chart )
    # ,sales_chart=sales_chart, rating_chart=rating_chart

          if analysis_results:
            return render_template('home.html',**context)
          
          else:
              results=scrape_fiverr(keyword, seller_type, seller_location,search_id)
              analysis_results = analyze_data(results)

              return render_template('home.html', results=analysis_results)
      return render_template('home.html')

















"""def construct_fiverr_url(keyword, seller_type=None, seller_country=None):
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

from selenium.webdriver.common.action_chains import ActionChains
def create_driver():
     chrome_options = Options()
     chrome_options.add_argument('--disable-gpu')
     chrome_options.add_argument('--no-sandbox')
     chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
     service = Service(chromedriver_path)
     driver = webdriver.Chrome(service=service, options=chrome_options)

    
     # Example of scrolling down to simulate user behavior
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     human_like_delay()
     action = ActionChains(driver)
     action.move_by_offset(100, 100).perform()
     human_like_delay()
     return driver
def scrape_fiverr(keyword, seller_type=None, seller_country=None):
     url = construct_fiverr_url(keyword, seller_type, seller_country)
     driver = create_driver()
     results = []
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
         print(f"Error during scraping: {e}")
     finally:
         driver.quit()
     return results
@app.route("/home", methods=['POST', 'GET'])
@login_required
def home():
     if request.method == "POST":
         keyword = request.form.get('keyword')
         seller_type = request.form.get('seller_type')
         seller_country = request.form.get('seller_country')
         results = scrape_fiverr(keyword, seller_type, seller_country)
         return render_template('home.html', results=results)
     return render_template('home.html')





"""

















# def scrape_fiverr(keyword, seller_type=None, seller_country=None):
#     url = construct_fiverr_url(keyword, seller_type, seller_country)
  
#     chrome_options = Options()
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--no-sandbox')
#     #chrome_options.add_argument('--headless')
#     #chrome_options.add_argument(f'--proxy-server={random.choice(proxies)}')
#     chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')    
#     chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Replace with your actual path
#     service = Service(chromedriver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     return driver
#     driver.get(url)  # human_like_delay()  # try:
#     WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper')))
#     except Exception as e:
#        print("Timed out waiting for page to load")
#        driver.quit()
#        return []  # results = []
#     try:
#        listings = driver.find_elements(By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper div.basic-gig-card')
#        for gig in listings:
#             try:
#                title_element = gig.find_element(By.CSS_SELECTOR, 'a > p')
#                title = title_element.get_attribute('innerText').strip()
#                print('Title:', title)
#                 url = gig.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
#                 price_element = gig.find_element(By.CSS_SELECTOR, 'a span span')
#                 price = price_element.text.strip().replace('\u00A0', ' ') if price_element else 'N/A'
#                 print("Price:", price)
#               results.append({'title': title, 'url': url, 'price': price})
#               human_like_delay()  # Add a delay between interactions
#             except Exception as e:
#                print(f"Error parsing gig: {e}")
#     except Exception as e:
#         print(f"Error locating gig listings: {e}")
#     driver.quit()

#     return results


