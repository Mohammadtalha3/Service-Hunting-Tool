from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set the path to the ChromeDriver executable
chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

# Create a Service object with the ChromeDriver path
service = Service(chromedriver_path)

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service)

# Open a website
driver.get("https://www.google.com")

# Print the title of the page
print(driver.title)

# Close the browser
driver.quit()
