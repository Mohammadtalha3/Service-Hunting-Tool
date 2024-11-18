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











    #def scrape_fiverr(keyword, seller_type=None, seller_country=None):
#     # Set up Chrome options
#     chrome_options = Options()
#     # chrome_options.add_argument('--headless')  # Uncomment to run in headless mode
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--no-sandbox')

#     # Initialize the Chrome driver
#     chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
#     service = Service(chromedriver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     # Navigate to Fiverr search page
#     search_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}"
#     driver.get(search_url)

#     # Apply filters for seller type if provided
#     if seller_type:
#         try:
#             print("Attempting to click the filter menu")
            
#             # Locating and expanding the filter menu step-by-step
#             main_wrapper = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, 'main-wrapper'))
#             )
#             print("Found main-wrapper")

#             main_content = main_wrapper.find_element(By.CLASS_NAME, 'main-content')
#             print("Found main-content")

#             zone_main = main_content.find_element(By.ID, '__ZONE__main')
#             print("Found __Zone__main")

#             search_perseus = zone_main.find_element(By.CLASS_NAME, 'search_perseus')
#             print("Found search_perseus")

#             listings_perseus = search_perseus.find_element(By.CLASS_NAME, 'listings-perseus')
#             print("Found listings-perseus")

#             search_page = listings_perseus.find_element(By.CSS_SELECTOR, 'div.search-page.top-filters')
#             print("Found search-page.top-filters")

#             listing_layout = search_page.find_element(By.CSS_SELECTOR, 'div._1jw9k7t14._1sz16f5s._7s6vff19.z58z870.z58z871f.listing-layout')
#             print("Found listing-layout")

#             sticky_wrapper = listing_layout.find_element(By.CLASS_NAME, 'sticky-wrapper')
#             print("Found sticky-wrapper")

#             shadow_effect = sticky_wrapper.find_element(By.CLASS_NAME, 'shadow-effect')
#             print("Found shadow-effect")

#             floating_top_bar = shadow_effect.find_element(By.CLASS_NAME, 'floating-top-bar')
#             print("Found floating-top-bar")

#             top_filters_inside = floating_top_bar.find_element(By.CLASS_NAME, 'top-filters')
#             print("Found top-filters inside floating-top-bar")

#             all_hfsWVMV = top_filters_inside.find_elements(By.CLASS_NAME, 'hfsWVMV')
#             print(f"Found {len(all_hfsWVMV)} elements with class 'hfsWVMV'")
#             if len(all_hfsWVMV) < 2:
#                 raise Exception("Less than 2 divs with class 'hfsWVMV' found")

#             expanded_div = all_hfsWVMV[1]
#             # expands_button= expanded_div.find_element(By.TAG_NAME, 'button')
#             # print(expands_button.get_attribute('class'))
#             # expands_button.click()
#             # print("Button pressed successfully")
#             # print(expanded_div.get_attribute('class'))
#             print(f"Expanded div found: {expanded_div}")
#             #expand_button = expanded_div.find_element(By.TAG_NAME, 'button')
#             try:
#                 if expanded_div.get_attribute('aria-expanded') == 'false':
#                     #human_like_delay()
#                     print(expanded_div.get_attribute('class'))
#                     print('yes it is false')
#                     #expand_button = expanded_div.find_element(By.TAG_NAME, 'button')
#                     # expand_button = WebDriverWait(expanded_div, 10).until(
#                     #     EC.element_to_be_clickable((By.TAG_NAME, 'button'))
#                     # )
#                     #driver.execute_script("arguments[0].scrollIntoView(true);", expanded_div)
#                     driver.execute_script("arguments[0].scrollIntoView(true);", expanded_div)
#                     print("Scrolled to the expanded_div")

#                     all_hfsWVMV = top_filters_inside.find_elements(By.CLASS_NAME, 'hfsWVMV')
#                     expanded_div = all_hfsWVMV[1]

#                     expand_button= expanded_div.find_element(By.TAG_NAME,'button')

#                     #human_like_delay()

#                     expand_button.click()
#                     human_like_delay()
#                     print('Expanded button was clicked')

                  

#                     try:
#             # Wait for the expanded div to have aria-expanded='true'
                        
#                         # Locate the newly visible menu
#                         drop_shadow_div = WebDriverWait(driver, 10).until(
#                             EC.presence_of_element_located((By.CSS_SELECTOR, 'div.drop-shadow-z2'))
#                         )
#                         human_like_delay()
#                         driver.execute_script("arguments[0].scrollIntoView(true);", drop_shadow_div)
#                         print("Expanded menu is visible and has been scrolled into view")

#                     except TimeoutException:
#                         print("Timeout waiting for the expanded menu to be visible")
#                     except StaleElementReferenceException:
#                         print("Stale element reference while waiting for the expanded menu")
#                     except Exception as e:
#                         print(f"Error while locating or scrolling to the expanded menu: {e}")
#             except TimeoutException:
                
#                 print("Timeout waiting for expand button to be clickable")
#             except Exception as e:
#                 print(f"Error: {e}")


#             human_like_delay()
#             if seller_type:
#                 checkbox_mapping = {
#                     'top_rated_seller': 'Top Rated Seller',
#                     'level_two_seller': 'Level Two Seller',
#                     'level_one_seller': 'Level One Seller',
#                     'New_seller': 'New Seller'
#                 }
#                 checkbox_label = checkbox_mapping.get(seller_type)
#                 if checkbox_label:
#                     try:
#                         filter_content = top_filters_inside.find_element(By.CSS_SELECTOR, 'div.drop-shadow-z2')
#                         menu_content = filter_content.find_element(By.CLASS_NAME, 'menu-content')
#                         content_scroll = menu_content.find_element(By.CLASS_NAME, 'content-scroll')
#                         checkbox_list = content_scroll.find_element(By.CSS_SELECTOR, 'div > div.checkbox-list')
#                         checkbox_labels = checkbox_list.find_elements(By.CLASS_NAME, 'tKumvjp.LFMwg3P.qFWrIB7.checkbox')

#                         for label in checkbox_labels:
#                             input_element = label.find_element(By.TAG_NAME, 'input')
#                             if input_element.get_attribute('name') == seller_type:
#                                 checkbox = label.find_element(By.CSS_SELECTOR, 'span.YgpbAto.checkmark-box > span.glAQDp5.QcGQdIt')
#                                 driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
#                                 javascript_click(driver,checkbox)
#                                 # checkbox.click()
#                                 print(f"Checkbox for {checkbox_label} selected")
#                                 break

#                     except TimeoutException:
#                         print("Timed out waiting for filter content to be visible")
#                     except Exception as e:
#                         print(f"Error selecting checkbox for {seller_type}: {e}")

#                 human_like_delay()
#                 random_mouse_movement(driver)

                

#                 try:
#                         apply_button = top_filters_inside.find_element(By.CSS_SELECTOR, 'div.menu-content div.button-row button.apply')
#                         #driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
#                         ensure_element_in_view(driver, apply_button)
#                         apply_button.click()
#                         #human_like_delay()
#                         #actions = ActionChains(driver)
#                         #actions.move_to_element(apply_button).click().perform()
#                         print("Clicked the Apply button")
#                 except TimeoutException:
#                         print("Timed out waiting for Apply button to be clickable")
#                 except Exception as e:
#                         print(f"Error clicking Apply button: {e}")

                        

#         except TimeoutException:
#             print("Timed out waiting for an element in the path")
#         except ElementClickInterceptedException:
#             print("ElementClickInterceptedException: Element is not clickable")
#         except Exception as e:
#             print(f"Error clicking on button: {e}")

#     # Apply filters for seller country if provided
#     if seller_country:
#         try:
#             print("Attempting to click the filter menu")
#             # Find and click the filter menu within div#topbar
#             filter_menu = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#topbar div.content-scroll > div > div.more-filter-item.with-carrot'))
#             )
#             print(f"Found filter menu: {filter_menu}")
#             filter_menu.click()
#             print("Clicked on seller country filter")

#             # Wait for filter options to be present
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, 'div.checkbox-list'))
#             )
#             print("Seller country filter options are present")

#             # Find the specific seller country filter option and click it
#             seller_country_filter = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), '{seller_country}')]"))
#             )
#             print(f"Found seller country filter option: {seller_country_filter}")
#             seller_country_filter.click()
#             print(f"Selected seller country: {seller_country}")
#         except TimeoutException:
#             print("Timed out waiting for seller country filter menu")
#         except ElementClickInterceptedException:
#             print("ElementClickInterceptedException: Element is not clickable")
#         except Exception as e:
#             print(f"Error applying seller country filter: {e}")

#     # Allow time for the page to reload after applying filters
#     time.sleep(5)

#     # Wait for the listings to load
#     try:
#         WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper')))
#     except Exception as e:
#         print("Timed out waiting for page to load")
#         driver.quit()
#         return []

#     # Parse the search results
#     results = []
#     try:
#         listings = driver.find_elements(By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper div.basic-gig-card')
#         for gig in listings:
#             try:
#                 title_element = gig.find_element(By.CSS_SELECTOR, 'a > p')
#                 title = title_element.get_attribute('innerText').strip()
#                 print(f'Title: {title}')
#                 url = gig.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
#                 price_element = gig.find_element(By.CSS_SELECTOR, 'a span span')
#                 price = price_element.text.strip().replace('\u00A0', ' ') if price_element else 'N/A'
#                 print(f'Price: {price}')
#                 results.append({'title': title, 'url': url, 'price': price})
#             except Exception as e:
#                 print(f"Error parsing gig: {e}")
#     except Exception as e:
#         print(f"Error locating gig listings: {e}")

#     # Close the browser
#     driver.quit()

#     return results












