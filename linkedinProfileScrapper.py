from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LinkedIn profile URL (the profile you want to scrape)
profile_url = input("Enter the profile url : ")  # add any linkedin's profile link

# Path to ChromeDriver executable
chrome_driver_path = r"E:/chromedriver-win64/chromedriver-win64/chromedriver.exe"  #location of the chrome driver 

# Set up the service
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the LinkedIn profile
driver.get(profile_url)

try:
    # Wait for the profile name to be visible (up to 20 seconds)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "top-card-layout__title"))
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

    # Extract the profile name
    try:
        name = driver.find_element(By.CLASS_NAME, "top-card-layout__title").text
        print(f"Name: {name}")
    except Exception:
        print("Name: Not available")

    # Get the headline (position and company, if public)
    try:
        headline = driver.find_element(By.CLASS_NAME, "top-card-layout__headline").text
        print(f"Headline: {headline}")
    except Exception:
        print("Headline: Not available")

    # Extract the location
    try:
        location = driver.find_element(By.CSS_SELECTOR, 'section.top-card-layout.container-lined .top-card-layout__entity-info-container h3 > div > div:nth-child(1) > span:nth-child(1)').text.strip()
        print(f"Location: {location}")
    except Exception:
        print("Location: Not available")

    # Extract the number of followers
    try:
        followers = driver.find_element(By.CSS_SELECTOR, 'section.top-card-layout.container-lined .top-card-layout__entity-info-container h3 > div > div:nth-child(3) > span:nth-child(1)').text.strip()
        print(f"Followers: {followers}")
    except Exception:
        print("Followers: Not available")

    # Extract the number of connections
    try:
        connections = driver.find_element(By.CSS_SELECTOR, 'section.top-card-layout.container-lined .top-card-layout__entity-info-container h3 > div > div:nth-child(3) > span:nth-child(2)').text.strip()
        print(f"Connections: {connections}")
    except Exception:
        print("Connections: Not available")

    # Extract the "About" section
    try:
        about = driver.find_element(By.CSS_SELECTOR, 'section.core-section-container.summary > div > p').text.strip()
        print(f"About: {about}")
    except Exception:
        print("About: Not available")

    # Extract and print each education entry
    try:
        education_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.education > div > ul > li')
        if education_items:
            for item in education_items:
                education_text = item.text.strip()
                print(f"Education: {education_text}")
        else:
            print("Education: Not available")
    except Exception:
        print("Education: Not available")

    # Extract and print each experience entry
    try:
        experience_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.experience > div > ul > li')
        if experience_items:
            for item in experience_items:
                experience_text = item.text.strip()
                print(f"Experience: {experience_text}")
        else:
            print("Experience: Not available")
    except Exception:
        print("Experience: Not available")
    # Extract and print each license and certification entry
    try:
        certifications_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.certifications > div > ul > li')
        if certifications_items:
            for item in certifications_items:
                # Extract the certification details
                certification_text = item.text.strip()
                print(f"License/Certification: {certification_text}")
                
                # Extract the link to the certificate, if available
                try:
                    certificate_link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    print(f"Certificate Link: {certificate_link}")
                except Exception:
                    print("Certificate Link: Not available")
        else:
            print("Licenses/Certifications: Not available")
    except Exception:
        print("Licenses/Certifications: Not available")

    # Extract languages
    try:
        language_elements = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.languages > div > ul > li')
        if language_elements:
            languages = [language.text.strip() for language in language_elements]
            print(f"Languages: {', '.join(languages)}")
        else:
            print("Languages: Not available")
    except Exception:
        print("Languages: Not available")
    
except Exception as e:
    print("Error extracting data or data not available publicly:", str(e))

# Close the browser
driver.quit()
