from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LinkedIn profile URL (the profile you want to scrape)
company_profile_url  = input("Enter the profile url : ")  # add any linkedin's profile link

# Path to ChromeDriver executable
chrome_driver_path = r"E:/chromedriver-win64/chromedriver-win64/chromedriver.exe"  #location of the chrome driver 

# Set up the service
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the LinkedIn profile
driver.get(company_profile_url)


try:
    # Wait for the page to load
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.top-card-layout__entity-info-container'))
    )
    # Close the modal if it appears
    try:
        modal_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#base-contextual-sign-in-modal > div > section > button'))
        )
        modal_button.click()
        print("Modal closed")
    except Exception:
        print("No modal found or couldn't close it")
    # Extract company name
    try:
        company_name = driver.find_element(By.CSS_SELECTOR, 'div.top-card-layout__entity-info-container h1').text.strip()
        print(f"Company Name: {company_name}")
    except Exception:
        print("Company Name: Not available")

    # Extract followers
    try:
        followers = driver.find_element(By.CSS_SELECTOR, 'div.top-card-layout__entity-info-container h3 > span').text.strip()
        print(f"Followers: {followers}")
    except Exception:
        print("Followers: Not available")

    # Extract about section
    try:
        about = driver.find_element(By.CSS_SELECTOR, 'section.core-section-container.my-3 p').text.strip()
        print(f"About: {about}")
    except Exception:
        print("About: Not available")

    # Extract company website
    try:
        company_website = driver.find_element(By.CSS_SELECTOR, 'dl > div:nth-child(1) > dd > a').get_attribute('href')
        print(f"Company Website: {company_website}")
    except Exception:
        print("Company Website: Not available")

    # Extract industry
    try:
        industry = driver.find_element(By.CSS_SELECTOR, 'dl > div:nth-child(2) > dd').text.strip()
        print(f"Industry: {industry}")
    except Exception:
        print("Industry: Not available")

    # Extract headquarters
    try:
        headquarters = driver.find_element(By.CSS_SELECTOR, 'dl > div:nth-child(4) > dd').text.strip()
        print(f"Headquarters: {headquarters}")
    except Exception:
        print("Headquarters: Not available")

    # Extract company type
    try:
        company_type = driver.find_element(By.CSS_SELECTOR, 'dl > div:nth-child(5) > dd').text.strip()
        print(f"Company Type: {company_type}")
    except Exception:
        print("Company Type: Not available")

    # Extract locations
    try:
        location_elements = driver.find_elements(By.CSS_SELECTOR, "section.core-section-container.locations > div > ul > li")
        for location_element in location_elements:
            location_text = location_element.text.strip()
            location_link = location_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(f"Location: {location_text}\nLink: {location_link}")
    except Exception:
        print("Locations: Not available")

    # Check for available jobs
    try:
        see_jobs_button = driver.find_element(By.CSS_SELECTOR, 'div.top-card-layout__entity-info-container a.top-card-layout__cta--primary')
        see_jobs_button.click()
        print("Navigating to Jobs page...")
        
        # Wait for the jobs list to load on the new page
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'section.two-pane-serp-page__results-list > ul > li'))
        )
        
        # Extract job details
        job_items = driver.find_elements(By.CSS_SELECTOR, 'section.two-pane-serp-page__results-list > ul > li')
        for job in job_items:
            job_title = job.find_element(By.CLASS_NAME, 'base-search-card__title').text.strip()
            job_address = job.find_element(By.CLASS_NAME, 'base-search-card__metadata').text.strip()
            job_link = job.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')
            print(f"Job Title: {job_title}\nJob Address: {job_address}\nJob Link: {job_link}\n")
    except Exception:
        print("Jobs not available for this company.")
    
except Exception as e:
    print("Error extracting data or data not available:", str(e))

# Close the browser
driver.quit()