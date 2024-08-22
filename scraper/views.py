from rest_framework.decorators import api_view
from rest_framework.response import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@api_view(["POST"])
def scrape_user_profile(request):
    profile_url = request.data.get("url")
    if not profile_url:
        return Response({"error": "URL is required"}, status=400)

    chrome_driver_path = r"E:/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Adjust this path if needed
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    result = {}
    try:
        driver.get(profile_url)
        
        # Wait for the page to load completely
        time.sleep(5)

        # Ensure modal is closed
        try:
            modal_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#base-contextual-sign-in-modal > div > section > button'))
            )
            modal_button.click()
            print("Modal closed")
        except Exception:
            print("No modal found or couldn't close it")

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "top-card-layout__title"))
        )

        # Extract the profile name
        try:
            result["name"] = driver.find_element(By.CLASS_NAME, "top-card-layout__title").text.strip()
        except Exception as e:
            result["name"] = "Not available"
            print(f"Error extracting name: {e}")

        # Extract the headline
        try:
            result["headline"] = driver.find_element(By.CLASS_NAME, "top-card-layout__headline").text.strip()
        except Exception as e:
            result["headline"] = "Not available"
            print(f"Error extracting headline: {e}")

        # Extract the location
        try:
            result["location"] = driver.find_element(
                By.CSS_SELECTOR, 'section.top-card-layout.container-lined .top-card-layout__entity-info-container h3 > div > div:nth-child(1) > span:nth-child(1)'
            ).text.strip()
        except Exception as e:
            result["location"] = "Not available"
            print(f"Error extracting location: {e}")

        # Extract the number of followers
        try:
            result["followers"] = driver.find_element(
                By.CSS_SELECTOR, 'section.top-card-layout.container-lined .top-card-layout__entity-info-container h3 > div > div:nth-child(3) > span:nth-child(1)'
            ).text.strip()
        except Exception as e:
            result["followers"] = "Not available"
            print(f"Error extracting followers: {e}")

        # Extract the "About" section
        try:
            about_section = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.summary > div > p')
            result["about"] = about_section[0].text.strip() if about_section else "Not available"
        except Exception as e:
            result["about"] = "Not available"
            print(f"Error extracting about section: {e}")

        # Extract education entries
        try:
            education_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.education > div > ul > li')
            result["education"] = [
                item.text.replace("\n", " ").strip() for item in education_items if item.text.strip()
            ] if education_items else ["Not available"]
        except Exception as e:
            result["education"] = ["Not available"]
            print(f"Error extracting education: {e}")

        # Extract experience entries
        try:
            experience_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.experience > div > ul > li')
            result["experience"] = [
                item.text.replace("\n", " ").strip() for item in experience_items if item.text.strip()
            ] if experience_items else ["Not available"]
        except Exception as e:
            result["experience"] = ["Not available"]
            print(f"Error extracting experience: {e}")
        # Extract certifications (if available)
        try:
            certifications_items = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.certifications > div > ul > li')
            result["certifications"] = [
                item.text.replace("\n", " ").strip() for item in certifications_items if item.text.strip()
            ] if certifications_items else "Not available"
        except Exception as e:
            result["certifications"] = "Not available"
            print(f"Error extracting certifications: {e}")

        # Extract languages (if available)
        try:
            language_elements = driver.find_elements(By.CSS_SELECTOR, 'section.core-section-container.languages > div > ul > li')
            result["languages"] = [
                language.text.replace("\n", " ").strip() for language in language_elements if language.text.strip()
            ] if language_elements else "Not available"
        except Exception as e:
            result["languages"] = "Not available"
            print(f"Error extracting languages: {e}")

    except Exception as e:
        result["error"] = str(e)
        
    finally:
        # Allow time to observe the window before it closes
        time.sleep(10)
        driver.quit()

    return Response(result)



# @api_view(["POST"])
# def scrape_company_profile(request):
#     company_url = request.data.get("url")
#     if not company_url:
#         return Response({"error": "URL is required"}, status=400)

#     chrome_driver_path = r"E:/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Adjust this path if needed
#     service = Service(executable_path=chrome_driver_path)
#     driver = webdriver.Chrome(service=service)

#     # Perform scraping
#     driver.get(company_url)
#     result = {}


