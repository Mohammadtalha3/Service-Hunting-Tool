from flask import render_template, url_for, flash, redirect, request
from app import app, db, login_manager
from forms import RegistrationForm, LoginForm
from models import User
from flask_login import login_user, current_user, logout_user, login_required
import bcrypt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time



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

@app.route("/home", methods=['POST', 'GET'])
@login_required
def home():
    if request.method== "POST":
        keyword= request.form.get('keyword')
        results = scrape_fiverr(keyword)
        return render_template('home.html', results= results)
    return render_template('home.html')

chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

def scrape_fiverr(keyword):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Initialize the Chrome driver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to Fiverr search page
    search_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}"
    driver.get(search_url)

    # Wait for the page to load completely
    time.sleep(5)

    # Parse the search results
    results = []
    gigs = driver.find_elements(By.CLASS_NAME, 'gig-card-layout')
    for gig in gigs:
        try:
            title_element = gig.find_element(By.CLASS_NAME, 'gig-title')
            title = title_element.text.strip()
            url = title_element.get_attribute('href')
            price_element = gig.find_element(By.CLASS_NAME, 'price')
            price = price_element.text.strip() if price_element else 'N/A'
            results.append({'title': title, 'url': url, 'price': price})
        except Exception as e:
            print(f"Error parsing gig: {e}")
    
    print(results)

    # Close the browser
    driver.quit()

    return results