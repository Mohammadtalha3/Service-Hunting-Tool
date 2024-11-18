from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_fiverr(keyword, seller_type=None, seller_country=None):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    chromedriver_path = "C:\\Users\\talha\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        search_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}"
        driver.get(search_url)

        # Apply filters for seller type if provided
        if seller_type:
            try:
                main_wrapper = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'main-wrapper'))
                )
                main_content = main_wrapper.find_element(By.CLASS_NAME, 'main-content')
                zone_main = main_content.find_element(By.ID, '__Zone__main')
                search_perseus = zone_main.find_element(By.CLASS_NAME, 'search_perseus')
                listings_perseus = search_perseus.find_element(By.CLASS_NAME, 'listings-perseus')
                search_page = listings_perseus.find_element(By.CSS_SELECTOR, 'div.search-page.top-filters')
                listing_layout = search_page.find_element(By.CSS_SELECTOR, 'div._1jw9k7t14._1sz16f5s._7s6vff19.z58z870.z58z871f.listing-layout')
                sticky_wrapper = listing_layout.find_element(By.CLASS_NAME, 'sticky-wrapper')
                shadow_effect = sticky_wrapper.find_element(By.CLASS_NAME, 'shadow-effect')
                floating_top_bar = shadow_effect.find_element(By.CLASS_NAME, 'floating-top-bar')
                top_filters_inside = floating_top_bar.find_element(By.CLASS_NAME, 'top-filters')
                all_hfsWVMV = top_filters_inside.find_elements(By.CLASS_NAME, 'hfsWVMV')
                if len(all_hfsWVMV) < 2:
                    raise Exception("Less than 2 divs with class 'hfsWVMV' found")

                expanded_div = all_hfsWVMV[1]
                if expanded_div.get_attribute('aria-expanded') == 'false':
                    expand_button = expanded_div.find_element(By.TAG_NAME, 'button')
                    driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
                    expand_button.click()

                filter_menu = WebDriverWait(expanded_div, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.z58z87275'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", filter_menu)
                filter_menu.click()

                if seller_type:
                    checkbox_mapping = {
                        'top_rated_seller': 'Top Rated Seller',
                        'level_two_seller': 'Level Two Seller',
                        'level_one_seller': 'Level One Seller',
                        'new_seller': 'New Seller'
                    }
                    checkbox_label = checkbox_mapping.get(seller_type)
                    if checkbox_label:
                        try:
                            filter_content = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div._9t04Hv.E_m9YLD.EHq3iYm.drop-shadow-z2'))
                            )
                            menu_content = filter_content.find_element(By.CLASS_NAME, 'menu-content')
                            content_scroll = menu_content.find_element(By.CLASS_NAME, 'content-scroll')
                            checkbox_list = content_scroll.find_element(By.CSS_SELECTOR, 'div > div.checkbox-list')
                            checkbox_labels = checkbox_list.find_elements(By.CLASS_NAME, 'tKumvjp.LFMwg3P.qFWrIB7.checkbox')

                            for label in checkbox_labels:
                                input_element = label.find_element(By.TAG_NAME, 'input')
                                if input_element.get_attribute('name') == seller_type:
                                    checkbox = label.find_element(By.CSS_SELECTOR, 'span.YgpbAto.checkmark-box > span.glAQDp5.QcGQdIt')
                                    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                                    checkbox.click()
                                    break

                        except TimeoutException:
                            print("Timed out waiting for filter content to be visible")
                        except Exception as e:
                            print(f"Error selecting checkbox for {seller_type}: {e}")

            except TimeoutException:
                print("Timed out waiting for an element in the path")
            except ElementClickInterceptedException:
                print("ElementClickInterceptedException: Element is not clickable")
            except Exception as e:
                print(f"Error clicking on button: {e}")

        # Apply filters for seller country if provided
        if seller_country:
            try:
                filter_menu = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#topbar div.content-scroll > div > div.more-filter-item.with-carrot'))
                )
                filter_menu.click()

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.checkbox-list'))
                )

                seller_country_filter = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), '{seller_country}')]"))
                )
                seller_country_filter.click()

            except TimeoutException:
                print("Timed out waiting for seller country filter menu")
            except ElementClickInterceptedException:
                print("ElementClickInterceptedException: Element is not clickable")
            except Exception as e:
                print(f"Error applying seller country filter: {e}")

        time.sleep(5)

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper')))
        except Exception as e:
            print("Timed out waiting for page to load")
            driver.quit()
            return []

        results = []
        try:
            listings = driver.find_elements(By.CSS_SELECTOR, 'div.gig-wrapper-impressions.gig-wrapper div.basic-gig-card')
            for gig in listings:
                try:
                    title_element = gig.find_element(By.CSS_SELECTOR, 'a > p')
                    title = title_element.get_attribute('innerText').strip()
                    url = gig.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    price_element = gig.find_element(By.CSS_SELECTOR, 'a span span')
                    price = price_element.text.strip().replace('\u00A0', ' ') if price_element else 'N/A'
                    results.append({'title': title, 'url': url, 'price': price})
                except Exception as e:
                    print(f"Error parsing gig: {e}")

        except Exception as e:
            print(f"Error getting gig listings: {e}")

        return results

    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

    finally:
        driver.quit()