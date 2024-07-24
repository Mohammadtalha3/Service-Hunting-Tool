from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with the path to your chromedriver
chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
service = Service(chromedriver_path)
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')  # run headless if needed
chrome_options.add_argument('--disable-dev-shm-usage')  # may fix some memory issues

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.fiverr.com/search/gigs?query=python")

    # Wait for floating-top-bar to appear
    floating_top_bar = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'floating-top-bar'))
    )
    print("Found floating-top-bar")

    # Locate top-filters inside floating-top-bar
    top_filters_inside = floating_top_bar.find_element(By.CLASS_NAME, 'top-filters')
    print("Found top-filters inside floating-top-bar")
    
    # Print the HTML source of top_filters_inside for debugging
    top_filters_html = top_filters_inside.get_attribute('outerHTML')
    print("HTML of top-filters div:")
    print(top_filters_html)

    # Get all direct child divs under top-filters
    all_divs = top_filters_inside.find_elements(By.XPATH, './div')
    print(f"Total direct child divs found: {len(all_divs)}")

    # Print all direct child divs for debugging
    for idx, div in enumerate(all_divs):
        print(f"Div {idx+1}: {div.get_attribute('outerHTML')}")

    # Interact with the fourth div if it exists
    if len(all_divs) > 3:
        target_div = all_divs[3]
        print("Fourth direct child div found:")
        print(target_div.get_attribute('outerHTML'))
        
        # Example interaction: clicking a button inside the div
        # Update the selector to match the actual button you need to interact with
        # button = target_div.find_element(By.CSS_SELECTOR, 'button.some-button-selector')
        # button.click()
    else:
        print("Less than 4 direct child divs found under top-filters")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
