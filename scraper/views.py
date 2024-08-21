from rest_framework.decorators import api_view
from rest_framework.response import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@api_view(["POST"])
def scrape_profile(request):
    profile_url = request.data.get("url")
    if not profile_url:
        return Response({"error": "URL is required"}, status=400)

    chrome_driver_path = r"E:/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Adjust this path if needed
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Perform scraping
    driver.get(profile_url)
    result = {}

    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "top-card-layout__title"))
        )

        # Extract the profile name
        try:
            name = driver.find_element(By.CLASS_NAME, "top-card-layout__title").text
            result["name"] = name
        except Exception:
            result["name"] = "Not available"

        # Extract the headline
        try:
            headline = driver.find_element(By.CLASS_NAME, "top-card-layout__headline").text
            result["headline"] = headline
        except Exception:
            result["headline"] = "Not available"

        # Extract the location
        try:
            location = driver.find_element(By.CSS_SELECTOR, 'section.top-card-layout.container-lined .top-card-layout__entity-info-container h3 > div > div:nth-child(1) > span:nth-child(1)').text.strip()
            result["location"] = location
        except Exception:
            result["location"] = "Not available"

        # Extract the number of followers
        try:
            followers = driver.find_element(By.CSS_SELECTOR, 'section.top-card-layout.container-lined .top-card-layout__entity-info-container h3 > div > div:nth-child(3) > span:nth-child(1)').text.strip()
            result["followers"] = followers
        except Exception:
            result["followers"] = "Not available"

        # Extract the "About" section
        try:
            about = driver.find_element(By.CSS_SELECTOR, 'section.core-section-container.summary > div > p').text.strip()
            result["about"] = about
        except Exception:
            result["about"] = "Not available"

        # Extract and print each education entry
        try:
            education_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.education > div > ul > li')
            result["education"] = [item.text.strip() for item in education_items] if education_items else "Not available"
        except Exception:
            result["education"] = "Not available"

        # Extract and print each experience entry
        try:
            experience_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.experience > div > ul > li')
            result["experience"] = [item.text.strip() for item in experience_items] if experience_items else "Not available"
        except Exception:
            result["experience"] = "Not available"

        # Extract and print each license and certification entry
        try:
            certifications_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.certifications > div > ul > li')
            if certifications_items:
                result["certifications"] = [
                    {"text": item.text.strip(), "link": item.find_element(By.TAG_NAME, 'a').get_attribute('href') if item.find_elements(By.TAG_NAME, 'a') else "Not available"}
                    for item in certifications_items
                ]
            else:
                result["certifications"] = "Not available"
        except Exception:
            result["certifications"] = "Not available"

        # Extract languages
        try:
            language_elements = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.languages > div > ul > li')
            result["languages"] = [language.text.strip() for language in language_elements] if language_elements else "Not available"
        except Exception:
            result["languages"] = "Not available"

    except Exception as e:
        result["error"] = str(e)

    finally:
        driver.quit()

    return Response(result)
